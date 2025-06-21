#include "shader.h"
#include <format>
#include <iostream>


#define MAX_LOG_LENGTH 1024
static char log[MAX_LOG_LENGTH];


GLint shader_load(const GLenum type, const std::string& source) {
	GLuint shader = glCreateShader(type);
	GLint compiled;

	if (shader == 0) {
		std::cerr << std::format("[ERROR]: could not create shader of type {}\n", type);
		return -1;
	}

	const char* c_str = source.c_str();
	glShaderSource(shader, 1, &c_str, NULL);

	glCompileShader(shader);
	glGetShaderiv(shader, GL_COMPILE_STATUS, &compiled);

	if (!compiled) {
		GLint info_len = 0;
		glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &info_len);
		glGetShaderInfoLog(shader, std::min(info_len, MAX_LOG_LENGTH), NULL, log);

		std::cerr << std::format("[ERROR]: compile error {}\n", log);

		glDeleteShader(shader);
	}

	return shader;
}


void shader_free(GLint shader_id) {
	glDeleteShader(shader_id);
}


GLint program_load(const std::string& vertex_shader_src,
		   const std::string& fragment_shader_src) {

	GLint vertex_shader = shader_load(GL_VERTEX_SHADER, vertex_shader_src);
	GLint fragment_shader = shader_load(GL_FRAGMENT_SHADER, fragment_shader_src);

	const auto program = program_load(vertex_shader, fragment_shader);

	shader_free(vertex_shader);
	shader_free(fragment_shader);

	return program;
}


GLint program_load(const GLint vertex_shader_id,
		   const GLint fragment_shader_id) {
	GLint program = glCreateProgram();
	GLint linked;

	if (program == 0) {
		std::cerr << std::format("[ERROR]: could not create program\n");
		return -1;
	}

	glAttachShader(program, vertex_shader_id);
	glAttachShader(program, fragment_shader_id);
	glLinkProgram(program);

	glGetProgramiv(program, GL_LINK_STATUS, &linked);

	if (!linked) {
		GLint info_len = 0;
		glGetProgramiv(program, GL_INFO_LOG_LENGTH, &info_len);
		glGetProgramInfoLog(program, std::min(info_len, MAX_LOG_LENGTH), NULL, log);

		std::cerr << std::format("[ERROR]: linker error {}\n", log);

		program_free(program);

		return -1;
	}

	return program;
}


void program_free(GLint program_id) {
	glDeleteProgram(program_id);
}
