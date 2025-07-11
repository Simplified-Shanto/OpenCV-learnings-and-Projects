---

### 🧮 Measuring the Angle Between Three Points in 2D

Given three points `P1`, `P2`, and `P3`, we want to measure the angle at `P2` formed by the lines **P1 → P2** and **P3 → P2**. The result should reflect whether it’s acute, obtuse, or reflex (i.e., in the full 0°–360° range).

---

### Step 1: Form Vectors

From the points, create two vectors pointing toward `P2`:

* **Vector A** = `P1 - P2` = $\vec{A} = (A_x, A_y)$
* **Vector B** = `P3 - P2` = $\vec{B} = (B_x, B_y)$

---

### Step 2: Use the Dot Product to Find the Angle

The **dot product** formula relates to the cosine of the angle between two vectors:

$$
\cos(\theta) = \frac{\vec{A} \cdot \vec{B}}{|\vec{A}||\vec{B}|}
$$

Where:

* $\vec{A} \cdot \vec{B} = A_x B_x + A_y B_y$
* $|\vec{A}| = \sqrt{A_x^2 + A_y^2}$
* $|\vec{B}| = \sqrt{B_x^2 + B_y^2}$

Then compute the angle using:

$$
\theta = \cos^{-1}\left(\frac{\vec{A} \cdot \vec{B}}{|\vec{A}||\vec{B}|}\right)
$$

This gives you an angle in radians between 0 and $\pi$ (i.e., 0° to 180°).

---

### Step 3: Use the 2D Cross Product to Get Direction

To determine if the angle is **clockwise** (>180°, reflex) or **counter-clockwise** (<180°), we use the **2D scalar cross product**:

$$
\text{cross}(A, B) = A_x B_y - A_y B_x
$$

Interpretation:

* If `cross > 0`, the turn from A to B is **counter-clockwise** → keep the angle
* If `cross < 0`, the turn is **clockwise** → angle should be $360^\circ - \theta$

---

### ✅ Final Python Code

```python
import math

def measureAngle(p1, p2, p3):
    # Vector A = P1 → P2
    A = (p1[0] - p2[0], p1[1] - p2[1])
    # Vector B = P3 → P2
    B = (p3[0] - p2[0], p3[1] - p2[1])

    # Dot product
    dot = A[0]*B[0] + A[1]*B[1]
    magA = math.hypot(A[0], A[1])
    magB = math.hypot(B[0], B[1])

    # Angle in radians
    angle_rad = math.acos(dot / (magA * magB))
    angle_deg = math.degrees(angle_rad)

    # Cross product to determine direction
    cross = A[0]*B[1] - A[1]*B[0]
    if cross < 0:
        angle_deg = 360 - angle_deg

    return angle_deg
```

---

### 🔍 Examples

```python
# Right angle
measureAngle((1, 0), (0, 0), (0, 1))  # Output: 90.0

# Reflex angle
measureAngle((-1, 0), (0, 0), (0, 1)) # Output: 270.0

# Straight line
measureAngle((1, 0), (0, 0), (-1, 0)) # Output: 180.0
```

---

