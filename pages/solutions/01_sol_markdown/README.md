# Rozwiązanie: Markdown — README

## Krótka podsekcja 1
To jest krótki tekst w pierwszej podsekcji. Zawiera przykładowe wzory inline: $a^2 + b^2 = c^2$, $e^{i\pi} + 1 = 0$ oraz $\int_0^1 x\,dx = \tfrac{1}{2}$.

## Krótka podsekcja 2
To jest drugi krótki tekst w innej podsekcji. Poniżej znajduje się obrazek, fragmenty tekstu w różnych stylach i listy.

**To jest pogrubiony fragment tekstu.**

*To jest fragment pochylony (italic).* 

~~To jest fragment przekreślony.~~

### Lista punktowana
- punkt pierwszy
- punkt drugi
- punkt trzeci

### Lista numerowana
1. pierwszy
2. drugi
3. trzeci

### Checklist (zadania)
- [x] zrobione
- [ ] do zrobienia
- [ ] opcjonalne

### Tabelka
| Kolumna A | Kolumna B | Kolumna C |
|-----------|-----------|-----------|
| Wartość 1 | Wartość 2 | Wartość 3 |
| 42        | 3.14      | tekst     |

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

### Wzory matematyczne — display math
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
