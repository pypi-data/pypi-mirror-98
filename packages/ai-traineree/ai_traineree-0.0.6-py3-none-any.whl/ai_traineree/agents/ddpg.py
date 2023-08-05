import torch
import torch.nn as nn

from ai_traineree import DEVICE
from ai_traineree.agents import AgentBase
from ai_traineree.agents.agent_utils import hard_update, soft_update
from ai_traineree.buffers import ReplayBuffer
from ai_traineree.loggers import DataLogger
from ai_traineree.networks.bodies import ActorBody, CriticBody
from ai_traineree.noise import GaussianNoise
from ai_traineree.utils import to_numbers_seq, to_tensor
from torch.optim import Adam
from torch.nn.functional import mse_loss
from typing import Dict, List, Optional


class DDPGAgent(AgentBase):
    """
    Deep Deterministic Policy Gradients (DDPG).

    Instead of popular Ornstein-Uhlenbeck (OU) process for noise this agent uses Gaussian noise.
    """

    name = "DDPG"

    def __init__(
        self,
        state_size: int,
        action_size: int,
        actor_lr: float=2e-3,
        critic_lr: float=2e-3,
        noise_scale: float=0.2,
        noise_sigma: float=0.1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.device = self._register_param(kwargs, "device", DEVICE)
        self.state_size = state_size
        self.action_size = action_size

        # Reason sequence initiation.
        hidden_layers = to_numbers_seq(self._register_param(kwargs, 'hidden_layers', (128, 128)))
        self.actor = ActorBody(state_size, action_size, hidden_layers=hidden_layers, gate_out=torch.tanh).to(self.device)
        self.critic = CriticBody(state_size, action_size, hidden_layers=hidden_layers).to(self.device)
        self.target_actor = ActorBody(state_size, action_size, hidden_layers=hidden_layers, gate_out=torch.tanh).to(self.device)
        self.target_critic = CriticBody(state_size, action_size, hidden_layers=hidden_layers).to(self.device)

        # Noise sequence initiation
        self.noise = GaussianNoise(shape=(action_size,), mu=1e-8, sigma=noise_sigma, scale=noise_scale, device=self.device)

        # Target sequence initiation
        hard_update(self.target_actor, self.actor)
        hard_update(self.target_critic, self.critic)

        # Optimization sequence initiation.
        self.actor_lr = float(self._register_param(kwargs, 'actor_lr', actor_lr))
        self.critic_lr = float(self._register_param(kwargs, 'critic_lr', critic_lr))
        self.actor_optimizer = Adam(self.actor.parameters(), lr=self.actor_lr)
        self.critic_optimizer = Adam(self.critic.parameters(), lr=self.critic_lr)
        self.max_grad_norm_actor = float(self._register_param(kwargs, "max_grad_norm_actor", 10.0))
        self.max_grad_norm_critic = float(self._register_param(kwargs, "max_grad_norm_critic", 10.0))
        self.action_min = float(self._register_param(kwargs, 'action_min', -1))
        self.action_max = float(self._register_param(kwargs, 'action_max', 1))
        self.action_scale = float(self._register_param(kwargs, 'action_scale', 1))

        self.gamma = float(self._register_param(kwargs, 'gamma', 0.99))
        self.tau = float(self._register_param(kwargs, 'tau', 0.02))
        self.batch_size = int(self._register_param(kwargs, 'batch_size', 64))
        self.buffer_size = int(self._register_param(kwargs, 'buffer_size', int(1e6)))
        self.buffer = ReplayBuffer(self.batch_size, self.buffer_size)

        self.warm_up = int(self._register_param(kwargs, 'warm_up', 0))
        self.update_freq = int(self._register_param(kwargs, 'update_freq', 1))
        self.number_updates = int(self._register_param(kwargs, 'number_updates', 1))

        # Breath, my child.
        self.reset_agent()
        self.iteration = 0
        self._loss_actor = 0.
        self._loss_critic = 0.

    def reset_agent(self) -> None:
        self.actor.reset_parameters()
        self.critic.reset_parameters()
        self.target_actor.reset_parameters()
        self.target_critic.reset_parameters()

    @property
    def loss(self) -> Dict[str, float]:
        return {'actor': self._loss_actor, 'critic': self._loss_critic}

    @loss.setter
    def loss(self, value):
        if isinstance(value, dict):
            self._loss_actor = value['actor']
            self._loss_critic = value['critic']
        else:
            self._loss_actor = value
            self._loss_critic = value

    @torch.no_grad()
    def act(self, obs, noise: float=0.0) -> List[float]:
        """Acting on the observations. Returns action.

        Returns:
            action: (list float) Action values.
        """
        obs = to_tensor(obs).float().to(self.device)
        action = self.actor(obs)
        action += noise*self.noise.sample()
        action = torch.clamp(action*self.action_scale, self.action_min, self.action_max)
        return action.cpu().numpy().tolist()

    def step(self, state, action, reward, next_state, done) -> None:
        self.iteration += 1
        self.buffer.add(state=state, action=action, reward=reward, next_state=next_state, done=done)

        if self.iteration < self.warm_up:
            return

        if len(self.buffer) > self.batch_size and (self.iteration % self.update_freq) == 0:
            for _ in range(self.number_updates):
                self.learn(self.buffer.sample())

    def compute_value_loss(self, states, actions, next_states, rewards, dones):
        next_actions = self.target_actor.act(next_states)
        assert next_actions.shape == actions.shape
        Q_target_next = self.target_critic.act(next_states, next_actions)
        Q_target = rewards + self.gamma * Q_target_next * (1 - dones)
        Q_expected = self.critic(states, actions)
        assert Q_expected.shape == Q_target.shape == Q_target_next.shape
        return mse_loss(Q_expected, Q_target)

    def compute_policy_loss(self, states) -> None:
        """Compute Policy loss based on provided states.

        Loss = Mean(-Q(s, _a) ),
        where _a is actor's estimate based on state, _a = Actor(s).
        """
        pred_actions = self.actor(states)
        return -self.critic(states, pred_actions).mean()

    def learn(self, experiences) -> None:
        """Update critics and actors"""
        rewards = to_tensor(experiences['reward']).float().to(self.device).unsqueeze(1)
        dones = to_tensor(experiences['done']).type(torch.int).to(self.device).unsqueeze(1)
        states = to_tensor(experiences['state']).float().to(self.device)
        actions = to_tensor(experiences['action']).to(self.device)
        next_states = to_tensor(experiences['next_state']).float().to(self.device)
        assert rewards.shape == dones.shape == (self.batch_size, 1)
        assert states.shape == next_states.shape == (self.batch_size, self.state_size)
        assert actions.shape == (self.batch_size, self.action_size)

        # Value (critic) optimization
        loss_critic = self.compute_value_loss(states, actions, next_states, rewards, dones)
        self.critic_optimizer.zero_grad()
        loss_critic.backward()
        nn.utils.clip_grad_norm_(self.critic.parameters(), self.max_grad_norm_critic)
        self.critic_optimizer.step()
        self._loss_critic = float(loss_critic.item())

        # Policy (actor) optimization
        loss_actor = self.compute_policy_loss(states)
        self.actor_optimizer.zero_grad()
        loss_actor.backward()
        nn.utils.clip_grad_norm_(self.actor.parameters(), self.max_grad_norm_actor)
        self.actor_optimizer.step()
        self._loss_actor = loss_actor.item()

        # Soft update target weights
        soft_update(self.target_actor, self.actor, self.tau)
        soft_update(self.target_critic, self.critic, self.tau)

    def state_dict(self) -> Dict[str, dict]:
        """Describes agent's networks.

        Returns:
            state: (dict) Provides actors and critics states.

        """
        return {
            "actor": self.actor.state_dict(),
            "target_actor": self.target_actor.state_dict(),
            "critic": self.critic.state_dict(),
            "target_critic": self.target_critic.state_dict()
        }

    def log_metrics(self, data_logger: DataLogger, step: int, full_log: bool=False):
        data_logger.log_value("loss/actor", self._loss_actor, step)
        data_logger.log_value("loss/critic", self._loss_critic, step)

        if full_log:
            for idx, layer in enumerate(self.actor.layers):
                if hasattr(layer, "weight"):
                    data_logger.create_histogram(f"actor/layer_weights_{idx}", layer.weight, step)
                if hasattr(layer, "bias") and layer.bias is not None:
                    data_logger.create_histogram(f"actor/layer_bias_{idx}", layer.bias, step)

            for idx, layer in enumerate(self.critic.layers):
                if hasattr(layer, "weight"):
                    data_logger.create_histogram(f"critic/layer_weights_{idx}", layer.weight, step)
                if hasattr(layer, "bias") and layer.bias is not None:
                    data_logger.create_histogram(f"critic/layer_bias_{idx}", layer.bias, step)

    def save_state(self, path: str):
        agent_state = dict(
            actor=self.actor.state_dict(), target_actor=self.target_actor.state_dict(),
            critic=self.critic.state_dict(), target_critic=self.target_critic.state_dict(),
            config=self._config,
        )
        torch.save(agent_state, path)

    def load_state(self, *, path: Optional[str]=None, agent_state: Optional[dict]=None):
        if path is None and agent_state:
            raise ValueError("Either `path` or `agent_state` must be provided to load agent's state.")
        if path is not None and agent_state is None:
            agent_state = torch.load(path)
        self._config = agent_state.get('config', {})
        self.__dict__.update(**self._config)

        self.actor.load_state_dict(agent_state['actor'])
        self.critic.load_state_dict(agent_state['critic'])
        self.target_actor.load_state_dict(agent_state['target_actor'])
        self.target_critic.load_state_dict(agent_state['target_critic'])
