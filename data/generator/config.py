from dataclasses import dataclass, field
from typing import Literal


DatasetStatus = Literal["DRAFT", "VALIDATED", "FROZEN", "RETIRED"]


@dataclass(frozen=True)
class DatasetSplitConfig:
    """Target workflow counts for one dataset split."""

    benign: int
    scam: int


@dataclass(frozen=True)
class ScamStrengthConfig:
    """Target distribution for generated scam workflows."""

    strong_fraction: float = 0.60
    moderate_fraction: float = 0.30
    noisy_fraction: float = 0.10


@dataclass(frozen=True)
class T1Config:
    """Synthetic generation parameters explicitly defined for T1."""

    min_account_age_days: int = 30
    max_account_age_days: int = 1000
    min_device_change_to_login_minutes: int = 0
    max_device_change_to_login_minutes: int = 2
    min_login_to_beneficiary_minutes: int = 1
    max_login_to_beneficiary_minutes: int = 5
    min_beneficiary_to_transfer_minutes: int = 1
    max_beneficiary_to_transfer_minutes: int = 5
    min_amount_multiplier: float = 1.5
    max_amount_multiplier: float = 4.0
    min_transfer_count: int = 1
    max_transfer_count: int = 2


@dataclass(frozen=True)
class GeneratorConfig:
    """Versioned configuration for a VYŪH synthetic dataset generation run."""

    dataset_id: str = "vyuh-synthetic"
    dataset_version: str = "0.1.0"
    generator_version: str = "0.1.0"
    schema_version: str = "0.1"
    config_version: str = "0.1.0"

    total_benign: int = 5000
    total_scam: int = 1000
    scam_cases_per_template: int = 200

    development_split: DatasetSplitConfig = field(
        default_factory=lambda: DatasetSplitConfig(benign=3000, scam=500)
    )
    golden_split: DatasetSplitConfig = field(
        default_factory=lambda: DatasetSplitConfig(benign=2000, scam=500)
    )

    hard_negative_fraction: float = 0.05
    hard_negative_fraction_max: float = 0.10

    scam_strength: ScamStrengthConfig = field(
        default_factory=ScamStrengthConfig
    )
    t1: T1Config = field(default_factory=T1Config)

    random_seed: int = 42
    status: DatasetStatus = "DRAFT"

    def validate(self) -> None:
        """Validate configuration invariants before generation."""
        if self.total_benign < 0 or self.total_scam < 0:
            raise ValueError("Dataset counts cannot be negative.")

        if self.scam_cases_per_template < 0:
            raise ValueError("Scam cases per template cannot be negative.")

        expected_scam = self.scam_cases_per_template * 5
        if expected_scam != self.total_scam:
            raise ValueError(
                "total_scam must equal scam_cases_per_template multiplied by 5 templates."
            )

        if (
            self.development_split.benign + self.golden_split.benign
            != self.total_benign
        ):
            raise ValueError(
                "Benign split counts must sum to total_benign."
            )

        if (
            self.development_split.scam + self.golden_split.scam
            != self.total_scam
        ):
            raise ValueError(
                "Scam split counts must sum to total_scam."
            )

        strength_total = (
            self.scam_strength.strong_fraction
            + self.scam_strength.moderate_fraction
            + self.scam_strength.noisy_fraction
        )
        if abs(strength_total - 1.0) > 1e-9:
            raise ValueError(
                "Scam-strength fractions must sum to 1.0."
            )

        if not 0 <= self.hard_negative_fraction <= self.hard_negative_fraction_max <= 1:
            raise ValueError(
                "Hard-negative fractions must satisfy 0 <= minimum <= maximum <= 1."
            )

        if self.t1.min_account_age_days > self.t1.max_account_age_days:
            raise ValueError("T1 account-age range is invalid.")

        if self.t1.min_amount_multiplier > self.t1.max_amount_multiplier:
            raise ValueError("T1 amount-multiplier range is invalid.")

        if self.t1.min_transfer_count > self.t1.max_transfer_count:
            raise ValueError("T1 transfer-count range is invalid.")


DEFAULT_CONFIG = GeneratorConfig()

if __name__ == "__main__":
    DEFAULT_CONFIG.validate()
    print(DEFAULT_CONFIG)