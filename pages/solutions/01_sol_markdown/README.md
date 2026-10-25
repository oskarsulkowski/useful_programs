# Markdown

## pierwsza podsekcja i krótki tekst

krótki tekst z 1 podsekcji

## druga podsekcja i krótki tekst

krótki tekst z 2 podsekcji

**pogrubiony fragment**

*fragment pochylony* 

~~fragment przekreślony~~

### Lista punktowana:
- punkt pierwszy
- punkt drugi
- punkt trzeci

### Lista numerowana:
1. pierwszy
2. drugi
3. trzeci

### Checklista:
- [x] pierwszy punkt
- [ ] drugi punkt
- [ ] trzeci punkt

### Tabelka
| Kolumna A | Kolumna B | Kolumna C |
|-----------|-----------|-----------|
| Wartość 1 | Wartość 2 | Wartość 3 |
| x         | y         | z         |

### Link do Google Colab
[Otwórz w Google Colab](http://colab.research.google.com)

### Krótki fragment kodu (Python)
```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)
plt.plot(x, y)
plt.title("Przykładowy wykres");
plt.savefig("wykres.png")
```

### Trzy wzory matematyczne w tekście 
$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$.

$\mathcal{F}\{f\}(\omega) = \int_{-\infty}^{\infty} f(t)\,e^{-i\omega t}\,dt$.

$\sum_{n=0}^{\infty} \frac{x^n}{n}$

### Wzory matematyczne jako wycentrowany blok
Poniżej trzy wzory jako oddzielne bloki wycentrowane:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

$$
\mathcal{F}\{f\}(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i \omega t}\,dt
$$

$$
\sum_{n=0}^{\infty} \frac{x^n}{n!} = e^{x}
$$

### Osadzony obrazek
![Wykres lokalny](wykres.png)
