#ifndef __SHADER_H__
#define __SHADER_H__


#include <string>

// I don't like this include because it's not right
// however I can't find easily another functioning include.
//
// I am currently using the CMake path for linking with OpenGL,
// this may not produce the expected results or may just use the
// core functionality (so no shader functionality)
//
// This is something I will have to understand and modify.
// I want to be able to select between two versions of OpenGL at the
// configuration step in CMake
#include <GLES2/gl2.h>


GLint shader_load(const GLenum type, const std::string& source);
void shader_free(GLint shader_id);

GLint program_load(const std::string& vertex_shader_src,
		   const std::string& fragment_shader_src);

GLint program_load(const GLint vertex_shader_id,
		   const GLint fragment_shader_id);

void program_free(GLint program_id);


#endif // __SHADER_H__
