def clamp(num, low,high):
    if num< low: return  low
    if num>high: return high
    return num

def rndint(num):
    return int(round(num))
