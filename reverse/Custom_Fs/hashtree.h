#ifndef HASHTREE__H

typedef struct TreeNode TreeNode;
typedef struct HashTree HashTree;

HashTree *new_hashtree(void);
TreeNode *new_node(uint64_t key, void *value); 
void *get_node_value(TreeNode *node);
uint64_t get_node_key(TreeNode *node);
int insert_hashtree(HashTree *t, TreeNode *n); 
TreeNode *find_hashtree(HashTree *t, uint64_t key); 
void dfs_hashtree(HashTree *t, void (*func)(TreeNode *, void *), void *ctx);
void serialize_hashtree(HashTree *h, void (*func)(void *, FILE *), FILE* fp); 
HashTree *deserialize_hashtree(void *(*func)(FILE *), FILE* fp); 
void free_node(TreeNode **n);
void free_hashtree(HashTree **t); 

#endif // !HASHTREE__H
