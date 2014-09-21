#encoding:utf-8
st1 = raw_input()
st2 = raw_input()

if isinstance(st1, str):
    st1 = st1.decode('utf-8')
if isinstance(st2, str):
    st2 = st2.decode('utf-8')
f = []
len1 = len(st1)
len2 = len(st2)

for i in range(len1 + 1):
    f.append([])
    for j in range(len2 + 1):
        f[i].append(0)

print f
for i in range(1, len1 + 1):
    for j in range(1, len2 + 1):
        if st1[i - 1] == st2[j - 1]:
            f[i][j] = f[i - 1][j - 1] + 1
        else:
            f[i][j] = max(f[i - 1][j], f[i][j - 1])
print f
