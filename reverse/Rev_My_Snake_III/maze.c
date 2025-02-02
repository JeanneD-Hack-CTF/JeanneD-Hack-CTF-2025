// Compile with: gcc `python3-config --ldflags --cflags` -shared -fPIC maze.c -o Maze.so
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <openssl/evp.h>

#define BASE_DELAY 50 * 1000
#define MAZE_USER  "Maze"

#define MAZE_WIDTH 16

// Globals 
static int player_x = 0;
static int player_y = 0;
static int flag_is_taken = 0;
// JDHACK{My_N4m3_1s_P13rr3_C4uch0n}
static unsigned char flag_enc[] = {
  0x32, 0xa8, 0x71, 0xcf, 0xd3, 0x3f, 0x52, 0x3d,
  0xb8, 0x46, 0xb1, 0x22, 0xdc, 0x96, 0x73, 0xaf,
  0x49, 0xed, 0x54, 0x2b, 0xb9, 0x18, 0x1a, 0x5d,
  0xd0, 0xad, 0x80, 0x3e, 0xb1, 0x61, 0x36, 0x05,
  0xb5, 0x64, 0x75, 0x7a, 0x59, 0xb1, 0xed, 0xdd, 
  0xc5, 0xb7, 0x64, 0xb9, 0x21, 0xcb, 0x00, 0x32,
};
static int flag_enc_len = 48;

EVP_MD_CTX *mdctx = NULL;

//P 11111111111111
//1 1        1   1
//1   11111 11 1 1
//1 111   1 1  1 1
//1 1   1 1 1 11 1
//1 1 111 1 1 1  1
//1     1 111 1 11
//11111 1     1 11
//1   1 1111111 11
//1 11111   21   1
//1 1   1 111111 1
//1 1 1   1    1 1
//1 1 111 11 1 1 1
//1 1   1 11 1 1 1
//1   1 1    1   1
//1111111111111111

unsigned char Maze[] = {
  0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
  1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1,
  1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1,
  1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1,
  1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1,
  1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1,
  1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1,
  1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1,
  1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
  1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 2, 1, 0, 0, 0, 1,
  1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1,
  1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1,
  1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
  1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
  1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1,
  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
};

void dialog(const char *user, const char *msg) {
  size_t size = strlen(msg);
  fprintf(stdout, "[%s] ", user);
  fflush(stdout);
  for (size_t i = 0; i < size; ++i) {
    fputc(msg[i], stdout);
    fflush(stdout);
    usleep(BASE_DELAY);
  }
  fputc('\n', stdout);
}

static int can_move_to(int x, int y) {
  // Check if the plaer move is in the bound of the maze 
  if (x < 0 || x >= MAZE_WIDTH || y < 0 || y >= MAZE_WIDTH) {
    return 0;
  }
  // Check if the player can move in the given position 
  if (Maze[x + y * MAZE_WIDTH] == 1) {
    return 0;
  }
  return 1;
}

static PyObject *is_finished(PyObject *self, PyObject *args) {
  if (Maze[player_x + player_y * MAZE_WIDTH] == 2 && flag_is_taken) {
    return PyLong_FromLong(1);
  }
  return PyLong_FromLong(0);
}

static PyObject *up(PyObject *self, PyObject *args) {
  char buffer[3];
  if (can_move_to(player_x, player_y - 1)) {
    dialog(MAZE_USER, "Going up");
    player_y -= 1;
    snprintf(buffer, 3, "%x%x", player_y, player_x);
    EVP_DigestUpdate(mdctx, buffer, 2);
  } else {
    dialog(MAZE_USER, "Cannot move up");
  }
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *down(PyObject *self, PyObject *args) {
  char buffer[3];
  if (can_move_to(player_x, player_y + 1)) {
    dialog(MAZE_USER, "Going down");
    player_y += 1;
    snprintf(buffer, 3, "%x%x", player_y, player_x);
    EVP_DigestUpdate(mdctx, buffer, 2);
  } else {
    dialog(MAZE_USER, "Cannot move down");
  }
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *right(PyObject *self, PyObject *args) {
  char buffer[3];
  if (can_move_to(player_x + 1, player_y)) {
    dialog(MAZE_USER, "Going right");
    player_x += 1;
    snprintf(buffer, 3, "%x%x", player_y, player_x);
    EVP_DigestUpdate(mdctx, buffer, 2);
  } else {
    dialog(MAZE_USER, "Cannot move right");
  }
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *left(PyObject *self, PyObject *args) {
  char buffer[3];
  if (can_move_to(player_x - 1, player_y)) {
    dialog(MAZE_USER, "Going left");
    player_x -= 1;
    snprintf(buffer, 3, "%x%x", player_y, player_x);
    EVP_DigestUpdate(mdctx, buffer, 2);
  } else {
    dialog(MAZE_USER, "Cannot move left");
  }
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *flag(PyObject *self, PyObject *args) {
  unsigned char buffer[1024];
  int buffer_len = 1024;
  int flag_len = 0; 
  unsigned char iv[] = "1234567887654321";
  // Should be equal to 56978950719ec0038e1673df34a6d79
  unsigned char md_value[EVP_MAX_MD_SIZE];
  unsigned int md_len;
  if (Maze[player_x + player_y * MAZE_WIDTH] == 2 && !flag_is_taken) {
    flag_is_taken = 1;
    EVP_DigestFinal_ex(mdctx, md_value, &md_len);
    EVP_MD_CTX_free(mdctx);

    // Setup decryption
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    EVP_DecryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, md_value, iv);
    EVP_DecryptUpdate(ctx, buffer, &buffer_len, flag_enc, flag_enc_len);
    flag_len = buffer_len;
    EVP_DecryptFinal_ex(ctx, buffer + buffer_len, &buffer_len);
    flag_len += buffer_len;
    buffer[flag_len] = 0;

    if (strncmp((char *)buffer, "JDHACK", 6) != 0) {
      dialog(MAZE_USER, "Mmm, The flag doesn't seem correct, are you sure you took the right path?");
    } else {
      dialog(MAZE_USER, "Here is your flag:");
      dialog(MAZE_USER, (char *)buffer);
    }
  }
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *generate(PyObject *self, PyObject *args) {
  dialog(MAZE_USER, "Generating Maze");
  // Init openssl engine 
  mdctx = EVP_MD_CTX_new();
  EVP_DigestInit_ex(mdctx, EVP_md5(), NULL);

  Py_INCREF(Py_None);
  return Py_None;
}

static PyMethodDef MazeMethods[] = {
  { "is_finished", is_finished, METH_VARARGS, "" },
  { "up", up, METH_VARARGS, "" },
  { "down", down, METH_VARARGS, "" },
  { "right", right, METH_VARARGS, "" },
  { "left", left, METH_VARARGS, "" },
  { "flag", flag, METH_VARARGS, "" },
  { "generate", generate, METH_VARARGS, ""},
  { NULL, NULL, 0, NULL}
};

static struct PyModuleDef MazeModule = {
  PyModuleDef_HEAD_INIT,
  "Maze",
  NULL,
  -1,
  MazeMethods
};

PyMODINIT_FUNC PyInit_Maze(void) {
  return PyModule_Create(&MazeModule);
}
