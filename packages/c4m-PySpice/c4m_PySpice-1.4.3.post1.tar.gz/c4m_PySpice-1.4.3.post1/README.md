This is a fork of [PySpice](https://github.com/FabriceSalvaire/PySpice). The purpose of this fork is to be able to publish a package on PyPi with extra changes without conflicting with the upstream project.

Patches added to this release:

* [#249](https://github.com/FabriceSalvaire/PySpice/pull/249): Changes to make it easier to use PySpice with a large archive of SPICE models
* [#256](https://github.com/FabriceSalvaire/PySpice/pull/256): Support for .nodeset type initial condition.
* [#258](https://github.com/FabriceSalvaire/PySpice/pull/258): Added spice library support
* [#271](https://github.com/FabriceSalvaire/PySpice/pull/271): PWL support improvements
* [#272](https://github.com/FabriceSalvaire/PySpice/pull/271): Add DC temperature sweep support.

In order to be able to coexist with upstream PySpice release, the PySpice module has been moved into the c4m namespace. So where one used the `PySpice` module in their code before, one has to now use `c4m.PySpice` to access code of this fork. For all other project resources like docs, examples etc. devert to the [upstream project](https://github.com/FabriceSalvaire/PySpice)

Only minimal testing has been done on this fork to verify functionality as used by [PDKMaster](https://gitlab.com/Chips4Makers/PDKMaster) is working properly.

