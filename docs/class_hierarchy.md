# Class Hierarchy

Viscope follows a layered architecture: **Instruments** → **Virtual System** → **GUI** → **Application**.

---

## Instrument Layer

### Base Instruments (`viscope/instrument/base/`)

```
BaseInstrument
├── BaseCamera
├── BaseLaser
├── BasePump
├── BaseStage
├── BaseSwitch
├── BaseSLM
├── BaseADetector
├── BaseProcessor
└── BaseSequencer
```

`BaseInstrument` is the root class for all hardware interfaces. It provides threading support (`flagLoop`, `worker`, `lock`) and the `connect()` / `disconnect()` / `setParameter()` / `getParameter()` interface that every instrument subclass implements.

### Virtual Instruments (`viscope/instrument/virtual/`)

Each virtual class inherits from the corresponding base and adds a `flagSetParameter` flag used by the virtual microscope to react to parameter changes.

```
BaseCamera      → VirtualCamera
BaseLaser       → VirtualLaser
BasePump        → VirtualPump
BaseStage       → VirtualStage
BaseSwitch      → VirtualSwitch
BaseSLM         → VirtualSLM
BaseADetector   → VirtualADetector
```

### Data Processors (`viscope/instrument/`)

```
BaseProcessor
└── ADetectorProcessor
```

`ADetectorProcessor` links a `BaseADetector` instance and processes its acquired stacks.

---

## Virtual System Layer (`viscope/virtualSystem/`)

```
BaseSystem
├── SimpleMicroscope
└── TwoCameraMicroscope

Sample          (standalone — used by BaseSystem)
Component       (standalone — static optical calculation methods)
```

`BaseSystem` owns a `Sample` and a dict of virtual devices. It runs a simulation loop that subclasses override via `calculateVirtualFrame()` to model microscope optics.

---

## GUI Layer (`viscope/gui/`)

```
QObject
└── BaseGUI
    ├── CameraGUI
    ├── LaserGUI
    ├── PumpGUI
    ├── StageGUI
    ├── SwitchGUI
    ├── ADetectorGUI
    ├── ADetectorViewGUI
    ├── AllDeviceGUI
    ├── CameraViewGUI
    ├── CameraView2GUI
    ├── HistogramGUI
    └── NapariGUI

napari / superqt
└── NapariViewer
└── ViewerWindow
```

`BaseGUI` adds rate-limited GUI refresh (`guiUpdateTimed`) on top of Qt's `QObject`. Device-specific subclasses use `@magicgui` to auto-generate parameter widgets.

---

## Application (`viscope/main.py`)

```
VISCOPE
└── owns: QApplication, WindowManager, ViewerWindow, [BaseGUI, ...]
```

`VISCOPE` is the top-level singleton that creates the Qt application, manages viewer windows, and registers GUI panels.

---

## Full Inheritance Summary

```
object
├── ThreadFlag
├── BaseInstrument
│   ├── BaseCamera
│   │   └── VirtualCamera
│   ├── BaseLaser
│   │   └── VirtualLaser
│   ├── BasePump
│   │   └── VirtualPump
│   ├── BaseStage
│   │   └── VirtualStage
│   ├── BaseSwitch
│   │   └── VirtualSwitch
│   ├── BaseSLM
│   │   └── VirtualSLM
│   ├── BaseADetector
│   │   └── VirtualADetector
│   ├── BaseProcessor
│   │   └── ADetectorProcessor
│   └── BaseSequencer
├── BaseSystem
│   ├── SimpleMicroscope
│   └── TwoCameraMicroscope
├── Sample
├── Component
└── QObject
    └── BaseGUI
        ├── CameraGUI
        ├── LaserGUI
        ├── PumpGUI
        ├── StageGUI
        ├── SwitchGUI
        ├── ADetectorGUI
        ├── ADetectorViewGUI
        ├── AllDeviceGUI
        ├── CameraViewGUI
        ├── CameraView2GUI
        ├── HistogramGUI
        └── NapariGUI
```
