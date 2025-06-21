#include <format>
#include <iostream>
#include "image.h"
#include "shader.h"
#include "window.h"
#include "texture.h"


const char* extract_filename_from_args(int argc, char* const argv[]) {
	if (argc < 2) {
		std::cerr << "[INFO]: no image provided, loading default image" << std::endl;
		return "../resources/einstein.jpeg";
	}

	return argv[1];
}


int main(int argc, char* argv[]) {
	const char* image_filename = extract_filename_from_args(argc, argv);
	std::cerr << std::format("[INFO]: loading \"{}\"", image_filename) << std::endl;

	if (window_init("SVD demo", 600, 600) > 0) {
		return 1;
	}
	window_set_key_callback(exit_on_escape_callback);

	texture_init();
	Image I = create_random_image(20, 20);
	const auto tex = texture_create_from_image(I);

	std::cerr << std::format("[INFO]: OpenGL version `{}`", window_get_opengl_version()) << std::endl;

	while (!window_should_close()) {
		int width, height;
		window_get_framebuffer_size(&width, &height);

		glViewport(0, 0, width, height);
		glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT);

		texture_render(tex);

		window_swap_buffers();
		window_poll_events();
	}

	texture_close();
	window_close();

	return 0;
}
