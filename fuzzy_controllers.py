import numpy as np
import skfuzzy as fuzz
from matplotlib import pyplot as plt
from skfuzzy import control as ctrl


class FuzzyErrorController:
    def __init__(self, plot_functions: bool = False) -> None:
        self.plot_functions = plot_functions

        self.controller = ctrl.ControlSystem()
        self.rules = []
        self.simulation = ctrl.ControlSystemSimulation(self.controller)

    def get_gain(self, error: float) -> float:
        self.simulation.input["error"] = error
        self.simulation.compute()
        return self.simulation.output["gain"]


class FuzzyProportionalController(FuzzyErrorController):
    def __init__(self, plot_functions: bool = False) -> None:
        super().__init__(plot_functions)

        # Input.
        self.error = ctrl.Antecedent(np.arange(0, 100, 1), "error")

        # Output.
        self.gain = ctrl.Consequent(np.arange(0, 3, 0.5), "gain")

        # Input Membership Functions.
        self.error["small"] = fuzz.trimf(self.error.universe, [0, 0, 30])
        self.error["medium"] = fuzz.trimf(self.error.universe, [10, 40, 80])
        self.error["large"] = fuzz.trimf(self.error.universe, [60, 100, 100])

        # Output Membership Functions.
        self.gain["small"] = fuzz.trimf(self.gain.universe, [0, 0, 2])
        # self.gain["medium"] = fuzz.trimf(self.gain.universe, [0.5, 1.5, 2.5])
        self.gain["large"] = fuzz.trimf(self.gain.universe, [1, 3, 3])

        if self.plot_functions:
            self.error.view()
            self.gain.view()
            plt.show()

        # Rules
        rule1 = ctrl.Rule(self.error["small"], self.gain["large"])
        rule2 = ctrl.Rule(self.error["medium"], self.gain["small"])
        rule3 = ctrl.Rule(self.error["large"], self.gain["small"])

        self.rules = [rule1, rule2, rule3, ]

        for rule in self.rules:
            self.controller.addrule(rule)

        self.simulation = ctrl.ControlSystemSimulation(self.controller)


class FuzzyIntegralController(FuzzyErrorController):
    def __init__(self, plot_functions: bool = False):
        super().__init__(plot_functions)

        # Input.
        self.error = ctrl.Antecedent(np.arange(0, 100, 1), "error")

        # Output.
        self.gain = ctrl.Consequent(np.arange(0.01, 0.1, 0.01), "gain")

        # Input Membership Functions.
        self.error["small"] = fuzz.trimf(self.error.universe, [0, 0, 30])
        self.error["medium"] = fuzz.trimf(self.error.universe, [10, 40, 80])
        self.error["large"] = fuzz.trimf(self.error.universe, [60, 100, 100])

        # Output Membership Functions.
        self.gain["small"] = fuzz.trimf(self.gain.universe, [0, 0, 0.04])
        self.gain["medium"] = fuzz.trimf(self.gain.universe, [0.02, 0.06, 0.1])
        self.gain["large"] = fuzz.trimf(self.gain.universe, [0.08, 0.1, 0.1])

        if self.plot_functions:
            self.error.view()
            self.gain.view()
            plt.show()

        # Rules
        rule1 = ctrl.Rule(self.error["small"], self.gain["small"])
        rule2 = ctrl.Rule(self.error["medium"], self.gain["medium"])
        rule3 = ctrl.Rule(self.error["large"], self.gain["large"])

        self.rules = [rule1, rule2, rule3, ]

        for rule in self.rules:
            self.controller.addrule(rule)

        self.simulation = ctrl.ControlSystemSimulation(self.controller)
