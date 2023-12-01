from datetime import timedelta

def time2str(t: timedelta) -> str:
    '''Convertit un timedelta en str

    Args:
        t (timedelta): timedelta a convertir

    Returns:
        str: Le timedelta converti en str
    '''
    return f'{max(t.seconds // 3600, 0):02d}:{max((t.seconds // 60) % 60, 0):02d}:{max(t.seconds % 60, 0):02d}'
