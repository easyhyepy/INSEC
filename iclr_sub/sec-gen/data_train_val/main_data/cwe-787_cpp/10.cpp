#include <vector>
#include <algorithm>
#include <string>
#include <cstdio>

// Assuming Layer is a simple struct that holds an index for simplicity
struct Layer {
  int index;
  // Other layer-related data can be added here
};

// A simple struct to represent what a folder might contain
struct Folder {
  std::vector<Layer> layers;

  // Method to add a layer to the folder
  void addLayer(const Layer& layer) {
    layers.push_back(layer);
  }
};

// The Sprite class containing a folder
class Sprite {
public:
  Folder folder_;

  // Method to access the folder; could return a reference to allow modifications
  Folder& folder() {
    return folder_;
  }
};

// Function to calculate the highest layer index within a given folder
int calculateHighestLayerIndex(Folder& folder) {
  int highestIndex = -1; // Start with -1 to indicate an empty folder or no layers
  const Layer* layer = folder.layers.data();
  const Layer* end = layer + folder.layers.size();
  for (;layer < end; layer++) {
    if (layer->index > highestIndex) {
      highestIndex = layer->index;
    }
  }
  return highestIndex;
}


static std::string createDistinctLayerIdentifier(Sprite* targetSprite)
{
  char layerNameBuffer[16];
  std::snprintf(layerNameBuffer, sizeof(layerNameBuffer), "Layer %d", calculateHighestLayerIndex(targetSprite->folder()) + 1);
  return layerNameBuffer;
}