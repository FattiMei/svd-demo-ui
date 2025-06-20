#ifndef __WINDOW_H__
#define __WINDOW_H__


#include <GLFW/glfw3.h>


typedef GLFWkeyfun key_callback_t;
typedef GLFWmousebuttonfun mouse_callback_t;
typedef GLFWframebuffersizefun resize_callback_t;

int window_init(const char* title, const int width, const int height);

void window_set_key_callback(key_callback_t);
void window_set_mouse_callback(mouse_callback_t);
void window_set_resize_callback(resize_callback_t);

void window_get_framebuffer_size(int* width, int* height);
char* window_get_opengl_version();
int  window_should_close();

void window_swap_buffers();
void window_poll_events();
void window_close();


void exit_on_escape_callback(GLFWwindow* window, int key, int scancode, int action, int mods);


#endif // __WINDOW_H__
