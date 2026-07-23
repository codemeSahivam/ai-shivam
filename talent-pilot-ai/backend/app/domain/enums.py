"""Domain enums."""

from __future__ import annotations

from enum import Enum


class Recommendation(str, Enum):
    STRONG_HIRE = "Strong Hire"
    HIRE = "Hire"
    CONSIDER = "Consider"
    REJECT = "Reject"


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
