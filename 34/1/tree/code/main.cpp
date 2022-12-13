#include <array>
#include <cstdio>
#include <set>
#include <vector>

enum NodeColor { red = 0, black = 2 };

struct Node {
  int delta;
  NodeColor color;
  Node *parent;
  Node *children[2];
  Node *nextNonChild;

  Node *left() { return children[0]; }

  Node *right() { return children[1]; }

  Node *getSibling() {
    if (parent == nullptr) return nullptr;

    if (parent->left() == this) {
      return parent->right();
    } else {
      return parent->left();
    }
  }

  Node *getGrandparent() {
    if (parent == nullptr) return nullptr;
    return parent->parent;
  }

  Node *getUncle() {
    if (getGrandparent() == nullptr) return nullptr;

    if (getGrandparent()->left() == parent) {
      return getGrandparent()->right();
    } else {
      return getGrandparent()->left();
    }
  }
};

class MagicTree {
  Node *root;
  std::vector<Node *> nodes;

 private:
  Node *traverseNode(Node *node, bool right) {
    if (node == nullptr) {
      node = root;

      while (node->children[right ^ 1] != nullptr) {
        node = node->children[right ^ 1];
      }

      return node;
    }

    if (node->children[right] != nullptr) {
      node = node->children[right];

      while (node->children[right ^ 1] != nullptr) {
        node = node->children[right ^ 1];
      }

      return node;
    }

    while (node->parent != nullptr && node->parent->children[right] == node) {
      node = node->parent;
    }

    node = node->parent;  // Could be null, that's fine
    return node;
  }

  Node *nextNode(Node *node) { return traverseNode(node, true); }

  Node *previousNode(Node *node) { return traverseNode(node, false); }

  long getDistance(Node *node) {
    long sum = 0;

    while (node != nullptr) {
      sum += node->delta;
      node = node->parent;
    }

    return sum;
  }

  void isolateSubtree(Node *node, Node *root, long distance, bool right) {
    bool left = right ^ 1;

    if (node->children[left] != nullptr) {
      node->children[left]->delta -= distance;
    }

    while (node != root) {
      bool fromRight = node->parent->children[right] == node;
      node = node->parent;

      if (fromRight) {
        node->delta -= distance;
        node->children[right]->delta += distance;
      }
    }
  }

  void rotateSubtree(Node *top, bool right) {
    bool left = right ^ 1;

    Node *child = top->children[left];
    Node *innerGrandchild = child->children[right];
    Node *parent = top->parent;

    child->children[right] = top;
    top->parent = child;

    top->children[left] = innerGrandchild;
    if (innerGrandchild != nullptr) {
      innerGrandchild->parent = top;
    }

    child->parent = parent;

    if (parent != nullptr) {
      if (parent->left() == top) {
        parent->children[0] = child;
      } else {
        parent->children[1] = child;
      }
    } else {
      root = child;
    }

    long a = top->delta;
    long b = child->delta;

    top->delta = -b;
    child->delta = a + b;
    if (innerGrandchild != nullptr) {
      innerGrandchild->delta += b;
    }
  }

  void rebalance(Node *node) {
    if (node->parent == nullptr) return;

    if (node->parent->color == black) return;

    if (node->parent == root) {
      root->color = black;
    }

    if (node->getUncle() == nullptr || node->getUncle()->color == red) {
      node->parent->color = black;

      if (node->getGrandparent() != nullptr) {
        node->getGrandparent()->color = red;

        if (node->getUncle() != nullptr) {
          node->getUncle()->color = black;
        }

        rebalance(node->getGrandparent());
      }

      return;
    }

    bool parentRightChild = node->getGrandparent()->right() == node->parent;

    if (node->parent->children[parentRightChild ^ 1] == node) {
      Node *nextNode = node->parent;
      rotateSubtree(node->parent, parentRightChild);
      node = nextNode;
    }

    node->parent->color = black;
    node->getGrandparent()->color = red;
    rotateSubtree(node->getGrandparent(), parentRightChild ^ 1);
  }

 public:
  MagicTree() : nodes() {
    root = new Node({0, black, nullptr, {nullptr, nullptr}, nullptr});
    nodes.push_back(root);
  }

  ~MagicTree() {
    for (Node *node : nodes) {
      delete node;
    }
  }

  long getDistance(int nodeId) { return getDistance(nodes.at(nodeId)); }

  void addNode(int parentId) {
    Node *parent = nodes.at(parentId);
    long distance = getDistance(parent) + 1;

    Node *node =
        new Node({0, red, nullptr, {nullptr, nullptr}, this->nextNode(parent)});
    nodes.push_back(node);

    if (parent->right() == nullptr) {
      parent->children[1] = node;
      node->parent = parent;
    } else {
      Node *insertPoint = parent->right();

      while (insertPoint->left() != nullptr) {
        insertPoint = insertPoint->left();
      }

      insertPoint->children[0] = node;
      node->parent = insertPoint;
    }

    node->delta = distance - getDistance(node->parent);
    rebalance(node);
  }

  void incrementLength(int nodeId, long distance) {
    Node *start = nodes.at(nodeId);
    Node *end = previousNode(start->nextNonChild);

    std::set<Node *> visitedNodes;

    for (Node *n = start; n != nullptr; n = n->parent) {
      visitedNodes.insert(n);
    }

    Node *commonParent;

    for (Node *n = end; n != nullptr; n = n->parent) {
      if (visitedNodes.find(n) != visitedNodes.end()) {
        commonParent = n;
        break;
      }
    }

    commonParent->delta += distance;
    isolateSubtree(start, commonParent, distance, true);
    isolateSubtree(end, commonParent, distance, false);
  }

  unsigned int size() { return nodes.size(); }
};

uint32_t readInt32() {
  unsigned char data[4];
  if (fread(data, sizeof(data[0]), sizeof(data), stdin) < sizeof(data)) {
    throw std::runtime_error("End of stream");
  }
  return data[0] | (data[1] << 8) | (data[2] << 16) | (data[3] << 24);
}

uint32_t readInt24() {
  unsigned char data[3];
  if (fread(data, sizeof(data[0]), sizeof(data), stdin) < sizeof(data)) {
    throw std::runtime_error("End of stream");
  }
  return data[0] | (data[1] << 8) | (data[2] << 16);
}

uint8_t readInt8() {
  unsigned char data[1];
  if (fread(data, sizeof(data[0]), sizeof(data), stdin) < sizeof(data)) {
    throw std::runtime_error("End of stream");
  }
  return data[0];
}

int main() {
  MagicTree tree;

  stdin = freopen(nullptr, "rb", stdin);

  unsigned int operationCount = readInt32();
  unsigned long lastAnswer = 0;

  for (unsigned long i = 0; i < operationCount; i++) {
    unsigned long operationCode = readInt24();
    operationCode += lastAnswer;
    operationCode %= 3ul * tree.size();

    unsigned char operationType = operationCode / tree.size();
    unsigned int nodeId = operationCode % tree.size();

    unsigned long edgeLength = readInt8();

    switch (operationType) {
      case 0:
        tree.addNode(nodeId);
        break;
      case 1:
        tree.incrementLength(nodeId, edgeLength);
        break;
      case 2:
        lastAnswer = tree.getDistance(nodeId);
        break;
    }
  }

  printf("%ld\n", lastAnswer);

  return 0;
}

// 0
//    1
//     2
//      3
//  4
//   5