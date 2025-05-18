https://www.cnblogs.com/weily09/p/18323713/gcd
![[../Attachment/pictures/Pasted image 20250415103240.png]]
```cpp
const int T = 1000;
const int M = 1000000;

int g[T][T], fac[M][3];
bitset<M> vis;
vector<int> pri;
void prework() {
  vis[0] = vis[1] = true;
  fac[1][0] = fac[1][1] = fac[1][2] = 1;
  for (int i = 2; i < M; ++i) {
    if (!vis[i]) {
      fac[i][0] = fac[i][1] = 1;
      fac[i][2] = i;
      pri.push_back(i);
    }
    for (int j : pri) {
      int mul = i * j;
      vis[mul] = true;
      fac[mul][0] = fac[i][0] * j;
      fac[mul][1] = fac[i][1];
      fac[mul][2] = fac[i][2];
      sort(fac[mul], fac[mul] + 3);
      if (i % j == 0)
        break;
    }
  }
  for (int i = 0; i < T; ++i)
    g[0][i] = g[i][0] = i;
  for (int i = 1; i < T; ++i)
    for (int j = 1; j <= i; ++j)
      g[i][j] = g[j][i] = g[j][i % j];
}
int gcd(int a, int b) {
  int ans = 1;
  for (int i = 0; i < 3; ++i) {
    int _ = fac[a][i] > T ? (b % fac[a][i] ? 1 : fac[a][i])
                          : g[fac[a][i]][b % fac[a][i]];
    b /= _;
    ans *= _;
  }
  return ans;
}
```