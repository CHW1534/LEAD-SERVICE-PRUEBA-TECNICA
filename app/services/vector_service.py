def embed(text: str) -> list[float]:
    if not text:
        return [0.0]
    return [len(text), len(text.split())]


def similarity(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0

    # similarity por cada dimensión
    sims = [
        1 - abs(a[i] - b[i]) / max(a[i], b[i])
        for i in range(len(a))
        if a[i] > 0 and b[i] > 0
    ]

    return sum(sims) / len(sims)
