#ifndef __TEXTURE_H__
#define __TEXTURE_H__


#include <GLFW/glfw3.h>
#include "image.h"


void texture_init();
GLuint texture_create();
GLuint texture_create_from_image(const Image& I);
void texture_load_image(GLuint id, const Image& I);

void texture_render(const GLuint id);

void texture_close();


#endif // __TEXTURE_H__
