from argparse import ArgumentParser

from motor import SimpleMotor, PIDMotor, FuzzyPIDMotor
from utils import save_history_dict, plot_histories



if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "--target-rpm",
        type=int,
        nargs="?",
        dest="target_rpm",
        default=70,
        required=True,
        help="Target RPM",
    )

    parser.add_argument(
        "--max-iter",
        type=int,
        nargs="?",
        dest="max_iter",
        default=20,
        required=False,
        help="The max number of iterations for the run",
    )

    args = parser.parse_args()

    config = {
        "target_rpm": 70,
        "iterations_limit": 20,
    }

    simple_motor = SimpleMotor(**config)

    pid_motor = PIDMotor(
        **config,
        k_p=2,
        k_i=0.01,
        k_d=0,
    )

    fuzzy_pid_motor = FuzzyPIDMotor(**config, plot_functions=False)

    simple_motor_rpm_history = simple_motor.run()
    pid_motor_rpm_history = pid_motor.run()
    fuzzy_pid_motor_rpm_history = fuzzy_pid_motor.run()

    rpm_history = {
        "simple_motor": simple_motor_rpm_history,
        "pid_motor": pid_motor_rpm_history,
        "fuzzy_pid_motor": fuzzy_pid_motor_rpm_history,
    }

    save_history_dict(rpm_history)

    plot_histories(
        history=rpm_history,
        xlabel="Iteration",
        ylabel="RPM",
        title="RPM History",
        save="rpm_history_plot.png"
    )
