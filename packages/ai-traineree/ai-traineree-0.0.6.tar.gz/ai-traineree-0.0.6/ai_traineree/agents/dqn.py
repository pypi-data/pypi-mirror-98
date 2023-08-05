import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from ai_traineree import DEVICE
from ai_traineree.agents import AgentBase
from ai_traineree.agents.agent_utils import soft_update
from ai_traineree.buffers import NStepBuffer, PERBuffer
from ai_traineree.loggers import DataLogger
from ai_traineree.networks import NetworkType, NetworkTypeClass
from ai_traineree.networks.heads import DuelingNet
from ai_traineree.utils import to_numbers_seq, to_tensor
from typing import Callable, Dict, Optional, Type, Sequence, Union


class DQNAgent(AgentBase):
    """Deep Q-Learning Network (DQN).

    The agent is not a vanilla DQN, although can be configured as such.
    The default config includes dual dueling nets and the priority experience buffer.
    Learning is also delayed by slowly copying to target nets (via tau parameter).
    Although NStep is implemented the default value is 1-step reward.

    There is also a specific implemntation of the DQN called the Rainbow which differs
    to this implementation by working on the discrete space projection of the Q(s,a) function.
    """

    name = "DQN"

    def __init__(
        self,
        input_shape: Union[Sequence[int], int],
        output_shape: Union[Sequence[int], int],
        network_fn: Callable[[], NetworkType]=None,
        network_class: Type[NetworkTypeClass]=None,
        state_transform: Optional[Callable]=None,
        reward_transform: Optional[Callable]=None,
        **kwargs
    ):
        """Initiates the DQN agent.

        Parameters:
            lr: (default: 1e-3) learning rate
            gamma: (default: 0.99) discount factor
            tau: (default: 0.002) soft-copy factor
            update_freq: (default: 1)
            batch_size: (default: 32)
            buffer_size: (default: 1e5)
            warm_up: (default: 0)
            number_updates: (default: 1)
            max_grad_norm: (default: 10)
            using_double_q: (default: True) Whether to use double Q value
            n_steps: (int: 1) N steps reward lookahead

        """
        super().__init__(**kwargs)

        self.device = self._register_param(kwargs, "device", DEVICE, update=True)
        self.input_shape: Sequence[int] = input_shape if not isinstance(input_shape, int) else (input_shape,)
        self.in_features: int = self.input_shape[0]
        self.output_shape: Sequence[int] = output_shape if not isinstance(output_shape, int) else (output_shape,)
        self.out_features: int = self.output_shape[0]

        self.lr = float(self._register_param(kwargs, 'lr', 3e-4))
        self.gamma = float(self._register_param(kwargs, 'gamma', 0.99))
        self.tau = float(self._register_param(kwargs, 'tau', 0.002))

        self.update_freq = int(self._register_param(kwargs, 'update_freq', 1))
        self.batch_size = int(self._register_param(kwargs, 'batch_size', 64, update=True))
        self.buffer_size = int(self._register_param(kwargs, 'buffer_size', int(1e5), update=True))
        self.warm_up = int(self._register_param(kwargs, 'warm_up', 0))
        self.number_updates = int(self._register_param(kwargs, 'number_updates', 1))
        self.max_grad_norm = float(self._register_param(kwargs, 'max_grad_norm', 10))

        self.iteration: int = 0
        self.buffer = PERBuffer(**kwargs)
        self.using_double_q = bool(self._register_param(kwargs, "using_double_q", True))

        self.n_steps = int(self._register_param(kwargs, 'n_steps', 1))
        self.n_buffer = NStepBuffer(n_steps=self.n_steps, gamma=self.gamma)

        hidden_layers = to_numbers_seq(self._register_param(kwargs, 'hidden_layers', (64, 64)))
        self.state_transform = state_transform if state_transform is not None else lambda x: x
        self.reward_transform = reward_transform if reward_transform is not None else lambda x: x
        if network_fn is not None:
            self.net = network_fn()
            self.target_net = network_fn()
        elif network_class is not None:
            self.net = network_class(self.input_shape, self.out_features, hidden_layers=hidden_layers, device=self.device)
            self.target_net = network_class(self.input_shape, self.out_features, hidden_layers=hidden_layers, device=self.device)
        else:
            self.net = DuelingNet(self.input_shape, self.output_shape, hidden_layers=hidden_layers, device=self.device)
            self.target_net = DuelingNet(self.input_shape, self.output_shape, hidden_layers=hidden_layers, device=self.device)
        self.optimizer = optim.Adam(self.net.parameters(), lr=self.lr)
        self._loss: float = float('inf')

    @property
    def loss(self) -> Dict[str, float]:
        return {'loss': self._loss}

    @loss.setter
    def loss(self, value):
        if isinstance(value, dict):
            value = value['loss']
        self._loss = value

    def reset(self):
        self.net.reset_parameters()
        self.target_net.reset_parameters()
        self.optimizer = optim.Adam(self.net.parameters(), lr=self.lr)

    def step(self, state, action, reward, next_state, done) -> None:
        """Letting the agent to take a step.

        On some steps the agent will initiate learning step. This is dependent on
        the `update_freq` value.

        Parameters:
            state: S(t)
            action: A(t)
            reward: R(t)
            nexxt_state: S(t+1)
            done: (bool) Whether the state is terminal.

        """
        self.iteration += 1
        state = to_tensor(self.state_transform(state)).float().to("cpu")
        next_state = to_tensor(self.state_transform(next_state)).float().to("cpu")
        reward = self.reward_transform(reward)

        # Delay adding to buffer to account for n_steps (particularly the reward)
        self.n_buffer.add(state=state.numpy(), action=[int(action)], reward=[reward], done=[done], next_state=next_state.numpy())
        if not self.n_buffer.available:
            return

        self.buffer.add(**self.n_buffer.get().get_dict())

        if self.iteration < self.warm_up:
            return

        if len(self.buffer) >= self.batch_size and (self.iteration % self.update_freq) == 0:
            for _ in range(self.number_updates):
                self.learn(self.buffer.sample())

            # Update networks only once - sync local & target
            soft_update(self.target_net, self.net, self.tau)

    def act(self, state, eps: float = 0.) -> int:
        """Returns actions for given state as per current policy.

        Parameters:
            state (array_like): current state
            eps (float): epsilon, for epsilon-greedy action selection

        Returns:
            Categorical value for the action.

        """
        # Epsilon-greedy action selection
        if self._rng.random() < eps:
            return self._rng.randint(0, self.out_features-1)

        state = to_tensor(self.state_transform(state)).float()
        state = state.unsqueeze(0).to(self.device)
        action_values = self.net.act(state)
        return int(torch.argmax(action_values.cpu()))

    def learn(self, experiences: Dict[str, list]) -> None:
        """Updates agent's networks based on provided experience.

        Parameters:
            experiences: Samples experiences from the experience buffer.

        """
        rewards = to_tensor(experiences['reward']).type(torch.float32).to(self.device)
        dones = to_tensor(experiences['done']).type(torch.int).to(self.device)
        states = to_tensor(experiences['state']).type(torch.float32).to(self.device)
        next_states = to_tensor(experiences['next_state']).type(torch.float32).to(self.device)
        actions = to_tensor(experiences['action']).type(torch.long).to(self.device)

        with torch.no_grad():
            Q_targets_next = self.target_net.act(next_states).detach()
            if self.using_double_q:
                _a = torch.argmax(self.net(next_states), dim=-1).unsqueeze(-1)
                max_Q_targets_next = Q_targets_next.gather(1, _a)
            else:
                max_Q_targets_next = Q_targets_next.max(1)[0].unsqueeze(1)
        Q_targets = rewards + self.n_buffer.n_gammas[-1] * max_Q_targets_next * (1 - dones)
        Q_expected: torch.Tensor = self.net(states).gather(1, actions)
        loss = F.mse_loss(Q_expected, Q_targets)

        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.net.parameters(), self.max_grad_norm)
        self.optimizer.step()
        self._loss = float(loss.item())

        if hasattr(self.buffer, 'priority_update'):
            error = Q_expected - Q_targets
            assert any(~torch.isnan(error))
            self.buffer.priority_update(experiences['index'], error.abs())

    def state_dict(self) -> Dict[str, dict]:
        """Describes agent's networks.

        Returns:
            state: (dict) Provides actors and critics states.

        """
        return {
            "net": self.net.state_dict(),
            "target_net": self.target_net.state_dict(),
        }

    def log_metrics(self, data_logger: DataLogger, step: int, full_log: bool=False):
        """Uses provided DataLogger to provide agent's metrics.

        Parameters:
            data_logger (DataLogger): Instance of the SummaryView, e.g. torch.utils.tensorboard.SummaryWritter.
            step (int): Ordering value, e.g. episode number.
            full_log (bool): Whether to all available information. Useful to log with lesser frequency.
        """
        data_logger.log_value("loss/agent", self._loss, step)

    def save_state(self, path: str) -> None:
        """Saves agent's state into a file.

        Parameters:
            path: String path where to write the state.

        """
        agent_state = dict(
            net=self.net.state_dict(),
            target_net=self.target_net.state_dict(),
            config=self._config,
        )
        torch.save(agent_state, path)

    def load_state(self, *, path: Optional[str]=None, agent_state: Optional[dict]=None) -> None:
        """Loads state from a file under provided path.

        Parameters:
            path: String path indicating where the state is stored.

        """
        if path is None and agent_state is None:
            raise ValueError("Either `path` or `agent_state` must be provided to load agent's state.")
        if path is not None:
            agent_state = torch.load(path)
        self._config = agent_state.get('config', {})
        self.__dict__.update(**self._config)

        self.net.load_state_dict(agent_state['net'])
        self.target_net.load_state_dict(agent_state['target_net'])

    def save_buffer(self, path: str) -> None:
        """Saves data from the buffer into a file under provided path.

        Parameters:
            path: String path where to write the buffer.

        """
        import json
        dump = self.buffer.dump_buffer(serialize=True)
        with open(path, 'w') as f:
            json.dump(dump, f)

    def load_buffer(self, path: str) -> None:
        """Loads data into the buffer from provided file path.

        Parameters:
            path: String path indicating where the buffer is stored.

        """
        import json
        with open(path, 'r') as f:
            buffer_dump = json.load(f)
        self.buffer.load_buffer(buffer_dump)
