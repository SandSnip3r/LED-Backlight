#include "EasyBMP.h"

#include <algorithm>
#include <array>
#include <fstream>
#include <functional>
#include <iostream>
#include <random>

using namespace std;

mt19937 createRandomEngine() {
  random_device rd;
  array<int, mt19937::state_size> seed_data;
  generate_n(seed_data.data(), seed_data.size(), ref(rd));
  seed_seq seq(begin(seed_data), end(seed_data));
  return mt19937(seq);
}

double colorDistanceBetweenPixels(const RGBApixel &p1, const RGBApixel &p2) {
  double dRed = p1.Red-p2.Red;
  double dGreen = p1.Green-p2.Green;
  double dBlue = p1.Blue-p2.Blue;
  return sqrt(dRed*dRed + dGreen*dGreen + dBlue*dBlue);
}

ostream& operator<<(ostream &stream, const RGBApixel &pixel) {
  stream << '(' << (int)pixel.Red << ',' << (int)pixel.Green << ',' << (int)pixel.Blue << ')';
  return stream;
}

RGBApixel getAverageColor(const BMP &image, const vector<pair<int,int>> &pixelsGroup) {
  double averageRed = accumulate(pixelsGroup.begin(), pixelsGroup.end(), 0, [&image](double runningSum, const pair<int,int> &pixelIndices){
    return runningSum + image.GetPixel(pixelIndices.first, pixelIndices.second).Red;
  }) / pixelsGroup.size();
  double averageGreen = accumulate(pixelsGroup.begin(), pixelsGroup.end(), 0, [&image](double runningSum, const pair<int,int> &pixelIndices){
    return runningSum + image.GetPixel(pixelIndices.first, pixelIndices.second).Green;
  }) / pixelsGroup.size();
  double averageBlue = accumulate(pixelsGroup.begin(), pixelsGroup.end(), 0, [&image](double runningSum, const pair<int,int> &pixelIndices){
    return runningSum + image.GetPixel(pixelIndices.first, pixelIndices.second).Blue;
  }) / pixelsGroup.size();
  RGBApixel p;
  p.Red = averageRed;
  p.Green = averageGreen;
  p.Blue = averageBlue;
  return p;
}

template <class CentroidIt, class PixelGroupIt>
void writeHtmlPage(CentroidIt centroidBegin, CentroidIt centroidEnd, PixelGroupIt pixelGroupBegin, PixelGroupIt pixelGroupEnd, int totalPixels) {
  const int kExpectedPixelsPerCluster = static_cast<double>(totalPixels) / distance(centroidBegin, centroidEnd);
  const std::string head = R"Delim(<!DOCTYPE html>
<html>
<body>)Delim";
  const std::string foot = R"Delim(</body>
</html>)Delim";
  ofstream htmlFile("colors.html");
  if (!htmlFile) {
    cerr << "Couldnt open file\n";
    return;
  }
  htmlFile << head << '\n';
  CentroidIt centroidIt = centroidBegin;
  PixelGroupIt pixelGroupIt = pixelGroupBegin;
  const int kRectWidth = 500;
  while (centroidIt != centroidEnd) {
    htmlFile << "<svg width=\"" << kRectWidth << "\" height=\"200\"><rect width=\"" << (kRectWidth * static_cast<double>(pixelGroupIt->size())/kExpectedPixelsPerCluster) << "\" height=\"200\" style=\"fill:rgb" << *centroidIt << ";\" />Sorry, your browser does not support inline SVG.</svg>" << '\n';
    htmlFile << "<br>\n";
    ++centroidIt;
    ++pixelGroupIt;
  }
  htmlFile << foot << '\n';
}

int main() {
  constexpr int kClusterCount=10;
  constexpr int kIterationCount=1000;
  BMP image;
  image.ReadFromFile("images.bmp");
  const int kWidth = image.TellWidth();
  const int kHeight =  image.TellHeight();
  cout << "Total pixels: " << kWidth*kHeight << '\n';
  mt19937 eng = createRandomEngine();
  uniform_int_distribution<int> widthDist(0,kWidth-1);
  uniform_int_distribution<int> heightDist(0,kHeight-1);

  array<RGBApixel, kClusterCount> centroidPixels;
  generate(centroidPixels.begin(), centroidPixels.end(), [&image, &widthDist, &heightDist, &eng](){
    return image.GetPixel(widthDist(eng), heightDist(eng));
  });
  cout << "Starting centroid pixels: ";
  for (int n=0; n<kClusterCount; ++n) {
    cout << centroidPixels[n] << ' ';
  }
  cout << '\n';

  array<vector<pair<int,int>>, kClusterCount> pixelsGroups;
  for (int i=0; i<kIterationCount; ++i) {
    //Clear out pixel groups
    for_each(pixelsGroups.begin(), pixelsGroups.end(), [](auto &i){ i.clear(); });
    //For each pixel, calculate which one it's closest too
    for (int x=0; x<kWidth; ++x) {
      for (int y=0; y<kHeight; ++y) {
        const auto &thisPixel = image.GetPixel(x,y);
        array<double,kClusterCount> distances;
        transform(centroidPixels.begin(), centroidPixels.end(), distances.begin(), [&thisPixel](auto centroidPixel){
          return colorDistanceBetweenPixels(thisPixel, centroidPixel);
        });
        auto minIt = min_element(distances.begin(), distances.end());
        pixelsGroups[std::distance(distances.begin(), minIt)].emplace_back(x,y);
      }
    }
    //Now, calculate the average color in each group
    transform(pixelsGroups.begin(), pixelsGroups.end(), centroidPixels.begin(), [&image](auto i){ return getAverageColor(image, i); });
    cout << "Iteration " << i << " centroid pixels: ";
    for (int n=0; n<kClusterCount; ++n) {
      cout << centroidPixels[n] << ' ';
    }
    cout << '\n';
  }
  writeHtmlPage(centroidPixels.begin(), centroidPixels.end(), pixelsGroups.begin(), pixelsGroups.end(), kWidth*kHeight);
  cout << "Final centroids: ";
  for (auto i : centroidPixels) {
    cout << i << ' ';
  }
  cout << '\n';
  return 0;
}