/**
 * Codes adopted from David Wang, https://github.com/zq-david-wang/linux-tools/tree/main/drivers/mremap
 * to test our live process migration
 */
#include <stdlib.h>
#include <stdio.h>
#include <set>

using namespace std;

int total = 0;
#define MAXN 1024
int que[MAXN];
#define MOD 1000000007

int main()
{
    void *p1 = malloc(10000000 * sizeof(char));
    long long v;
    set<int> rs;
    int h = 0, i, ni, vv, rk;
    while (1)
    {
        printf("number>:");
        scanf("%lld", &v);
        if (v <= 0)
        {
            printf("You have entered %d numbers.\n", total);
            if (total)
            {
                printf("Entered numbers are:");
                for (i = 0; i < 8 && i < total; i++)
                {
                    ni = h - 1 - i;
                    if (ni < 0)
                        ni += MAXN;
                    printf(" %d", que[ni]);
                }
                printf("\n");
            }
        }
        else
        {
            que[h++] = v;
            if (h >= MAXN)
                h = 0;
            total++;
            vv = (v * 37) % MOD;
            rs.insert(vv);
            auto y = rs.lower_bound(vv);
            rk = 0;
            for (auto x = rs.begin(); x != y; x++)
                rk++;
        }
    }
    free(p1);
    return 0;
}
