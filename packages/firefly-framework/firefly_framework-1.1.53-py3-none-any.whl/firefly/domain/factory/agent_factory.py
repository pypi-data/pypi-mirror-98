#  Copyright (c) 2019 JD Williams
#
#  This file is part of Firefly, a Python SOA framework built by JD Williams. Firefly is free software; you can
#  redistribute it and/or modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#
#  Firefly is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details. You should have received a copy of the GNU Lesser General Public
#  License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  You should have received a copy of the GNU General Public License along with Firefly. If not, see
#  <http://www.gnu.org/licenses/>.

from __future__ import annotations

from typing import Dict

import firefly_di as di
from firefly.domain.factory.factory import T
from firefly.domain.service.core.agent import Agent

from .factory import Factory
from ..error import ConfigurationError


class AgentFactory(Factory[Agent]):
    def __init__(self, agents: Dict[str, Agent]):
        self._agents = agents

    def __call__(self, provider: str) -> T:
        if provider not in self._agents:
            raise ConfigurationError(f'No agent registered for provider "{provider}"')
        return self._agents[provider]

    def register(self, provider: str, agent: Agent):
        self._agents[provider] = agent
