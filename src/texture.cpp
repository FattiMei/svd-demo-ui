#include "texture.h"
#include "shader.h"
#include <vector>
#include <cassert>
#include <iostream>


static GLint program;


static const float vertices[] = {
	-1.0f, -1.0f, 0.0f,
	-1.0f,  1.0f, 0.0f,
	 1.0f, -1.0f, 0.0f,
	-1.0f,  1.0f, 0.0f,
	 1.0f,  1.0f, 0.0f,
	 1.0f, -1.0f, 0.0f
};


static const float texture_vertices[] = {
	0.0f, 0.0f,
	0.0f, 1.0f,
	1.0f, 0.0f,
	0.0f, 1.0f,
	1.0f, 1.0f,
	1.0f, 0.0f,
};


static const GLchar vertex_shader_src[] = R"(
	attribute vec3 position;
	attribute vec2 atexCoord;

	varying vec2 texCoord;

	void main() {
		gl_Position = vec4(position, 1.0);
		texCoord = atexCoord;
	}
)";


static const GLchar fragment_shader_src[] = R"(
	precision mediump float;

	varying vec2 texCoord;
	uniform sampler2D tex;

	void main() {
		vec4 c = texture2D(tex, texCoord);
		gl_FragColor = vec4(c.w, c.w, c.w, 1.0);
	}
)";


void texture_init() {
	program = program_load(vertex_shader_src, fragment_shader_src);
	glBindAttribLocation(program, 0, "position");
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, vertices);

	glBindAttribLocation(program, 1, "atexCoord");
	glEnableVertexAttribArray(1);
	glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, texture_vertices);
}


GLuint texture_create() {
	GLuint result;

	glGenTextures(1, &result);
	glBindTexture(GL_TEXTURE_2D, result);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);	
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

	return result;
}


GLuint texture_create_from_image(const Image& I) {
	const GLuint texture = texture_create();

	texture_load_image(texture, I);

	return texture;
}


void texture_load_image(GLuint id, const Image& I) {
	const int w = I.get_width();
	const int h = I.get_height();

	glBindTexture(GL_TEXTURE_2D, id);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_ALPHA, w, h, 0, GL_ALPHA, GL_UNSIGNED_BYTE, I.get_data());

	GLenum err = glGetError();
	assert(err == 0);

	glGenerateMipmap(GL_TEXTURE_2D);
}


void texture_render(const GLuint texture) {
	glBindTexture(GL_TEXTURE_2D, texture);
	glUseProgram(program);
	glDrawArrays(GL_TRIANGLES, 0, 6);
}


void texture_free(GLuint id) {
	glDeleteTextures(1, &id);
}


void texture_close() {
	program_free(program);
}
