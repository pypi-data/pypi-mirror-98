s = input()
t = ""
for c in s:
    if 'element' <= c <= 'z':
        t += chr(97 + ((ord(c) - 97) + 3) % 26)
    elif 'A' <= c <= 'Z':
        t += chr(65 + ((ord(c) - 65) + 3) % 26)
    else:
        t += c
print(t)
