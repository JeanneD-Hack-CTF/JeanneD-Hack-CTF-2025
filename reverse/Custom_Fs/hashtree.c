#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h> 
#include <string.h>

#include "hashtree.h"

#define EXIT_SUCCESS          0
#define EXIT_ERROR           -1

#define EMPTY_NODE_MARKER     0xffffffffffffffff

struct TreeNode {
  uint64_t  key;      // Key of the node 
  void     *value;    // Value of the node
  TreeNode *left;     // Left children of this node 
  TreeNode *right;    // Right children of this node
};

struct HashTree {
  uint64_t size;      // The number of element in the HashTree
  TreeNode *root;     // Pointer to the root of the tree
};

HashTree *new_hashtree(void) {
  HashTree *t = malloc(sizeof(*t));
  if (t != NULL) {
    t->size = 0;
    t->root = NULL;
  }
  return t;
}

TreeNode *new_node(uint64_t key, void *value) {
  TreeNode *node = malloc(sizeof(*node));
  if (node != NULL) {
    node->key = key;
    node->value = value;
    node->left = NULL;
    node->right = NULL;
  }
  return node;
}

void *get_node_value(TreeNode *node) {
  return node == NULL ? NULL : node->value;
}

uint64_t get_node_key(TreeNode *node) {
  return node == NULL ? 0 : node->key;
}

int insert_hashtree(HashTree *t, TreeNode *n) {
  int result = EXIT_ERROR;
  if (t != NULL && n != NULL) {
    TreeNode *parent = NULL;
    TreeNode *ptr = t->root;
    while (ptr != NULL) {
      if (ptr->key == n->key) {
        // Element exists in the tree 
        break;
      } else if (ptr->key > n->key) {
        // Visit left node 
        parent = ptr;
        ptr = ptr->left;
      } else {
        // Visit right node
        parent = ptr;
        ptr = ptr->right;
      }
    }

    // We either reach the end of the tree or the node already exists
    if (parent == NULL) {
      // No node in the tree
      t->root = n;
      ++(t->size);
      result = EXIT_SUCCESS;
    } else if (ptr == NULL) {
      if (n->key < parent->key) {
        // Insert left 
        parent->left = n;
      } else {
        // Insert right
        parent->right = n;
      }
      ++(t->size);
      result = EXIT_SUCCESS;
    } else {
      // nothing needed
    }
  }
  return result;
}

// Find a node in the HashTree based on it's key, if the 
TreeNode *find_hashtree(HashTree *t, uint64_t key) {
  TreeNode *ptr = NULL;
  if (t != NULL) {
    ptr = t->root;
    while (ptr != NULL) {
      if (ptr->key == key) {
        // Element exists in the tree 
        break;
      } else if (ptr->key > key) {
        // Visit left node 
        ptr = ptr->left;
      } else {
        // Visit right node
        ptr = ptr->right;
      }
    }
  }
  return ptr;
}

void __dfs_hashnode(TreeNode *n, void (*func)(TreeNode *, void *), void *ctx) {
  if (n != NULL) {
    // Depth first traversal 
    __dfs_hashnode(n->left, func, ctx);
    func(n, ctx);
    __dfs_hashnode(n->right, func, ctx);
  }
}

// General depth first traversal 
void dfs_hashtree(HashTree *t, void (*func)(TreeNode *, void *), void *ctx) {
  if (t != NULL && func != NULL) {
    __dfs_hashnode(t->root, func, ctx);
  }
}

void serialize_node(TreeNode *n, void (*func)(void *, FILE *), FILE* fp) {
  // If current node is NULL, store marker
  uint64_t key; 
  if (n == NULL) {
    key = EMPTY_NODE_MARKER;
    fwrite(&key, sizeof(key), 1, fp);
    return;
  }
 
  // Preorder traversal
  key = n->key;
  fwrite(&key, sizeof(key), 1, fp);
  func(n->value, fp);
  serialize_node(n->left, func, fp);
  serialize_node(n->right, func, fp);
}

void deserialize_node(TreeNode **n, void *(*func)(FILE *), FILE* fp) {
  uint64_t key;
  fread(&key, sizeof(key), 1, fp);

  // Check for maker 
  if (key == EMPTY_NODE_MARKER) {
    return;
  }

  // Read value 
  void *value = func(fp);
  if (value == NULL) {
    return;
  }
  *n = new_node(key, value);
  if (*n != NULL) {
    deserialize_node(&((*n)->left), func, fp);
    deserialize_node(&((*n)->right), func, fp);
  }
  
}

// This function stores a tree in a file pointed by fp
void serialize_hashtree(HashTree *h, void (*func)(void *, FILE *), FILE* fp) {
  if (h != NULL && func != NULL && fp != NULL) {
    fwrite(&h->size, sizeof(h->size), 1, fp);
    serialize_node(h->root, func, fp);
  }
}

// This function create a tree from the file pointed by fp
HashTree *deserialize_hashtree(void *(*func)(FILE *), FILE* fp) {
  HashTree *h = new_hashtree();
  if (h != NULL) {
    if (fread(&(h->size), sizeof(h->size), 1, fp) != 1) {
      free(h);
      h = NULL;
    } else {
      deserialize_node(&(h->root), func, fp);
    }
  }
  return h;
}

void free_node(TreeNode **n) {
  if (n != NULL && *n != NULL) {
    free(*n);
    *n = NULL;
  }
}
void __free_hashnode(TreeNode *n, void *unused) {
  if (n != NULL) {
    free_node(&n);
  }
}

void free_hashtree(HashTree **t) {
  if (t != NULL && *t != NULL) {
    dfs_hashtree(*t, __free_hashnode, NULL);
    free(*t);
    *t = NULL;
  }
}


