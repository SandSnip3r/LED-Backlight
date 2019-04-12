#include <cmath>
#include <iostream>

using namespace std;

int main(int argc, char *argv[]) {
  if (argc < 2) {
    cout << "no\n";
    return 1;
  }
  const int kScreenWidth=atoi(argv[1]);
  constexpr int kLedCount=3;
  const int kHeight = 1;//std::round(kScreenWidth/static_cast<float>(kLedCount));
  const int groupWidthCeil = std::ceil(kScreenWidth/static_cast<float>(kLedCount));
  const int groupWidthFloor = std::floor(kScreenWidth/static_cast<float>(kLedCount));
  const int remainder = kScreenWidth%kLedCount;
  int groupSize[kLedCount] = {};
  for (int i=0; i<kScreenWidth*kHeight; ++i) {
    const int kPixelColumn = i%kScreenWidth;
    int borderBetweenDifferentGroupSizes = (remainder)*groupWidthCeil;
    if (kPixelColumn < borderBetweenDifferentGroupSizes) {
      //Groups of size groupWidthCeil
      ++groupSize[kPixelColumn/groupWidthCeil];
    } else {
      //Groups of size groupWidthFloor
      ++groupSize[(kPixelColumn-remainder)/groupWidthFloor];
    }
  }
  for (int i=0; i<kLedCount; ++i) {
    cout << i << ' ' << groupSize[i] << '\n';
  }
  return 0;
}