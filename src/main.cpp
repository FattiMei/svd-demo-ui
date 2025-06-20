#include <format>
#include <vector>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <GLFW/glfw3.h>
#include "window.h"


int main(int argc, char* argv[]) {
	const char* image_name = "resources/einstein.jpeg";
	if (argc < 2) {
		std::cerr << "[INFO]: no image provided, loading default image" << std::endl;
	}
	else {
		image_name = argv[1];
	}

	std::cerr << std::format("[INFO]: loading \"{}\"", image_name) << std::endl;

	if (window_init("SVD demo", 600, 600) > 0) {
		return 1;
	}
	window_set_key_callback(exit_on_escape_callback);

	std::cerr << std::format("[INFO]: OpenGL version `{}`", window_get_opengl_version()) << std::endl;


	// ---------------------------- interactivity section ------------------------
	auto start_time = glfwGetTime();
	size_t frame_count = 0;

	while (!window_should_close()) {
		// frame time logic, just to have a measure of the smoothness of the UI
		const auto end_time = glfwGetTime();
		const auto delta_t = end_time - start_time;

		if (delta_t > 1.0) {
			const auto fps = static_cast<double>(frame_count) / delta_t;
			const auto avg_frame_time = delta_t / frame_count;

			std::cout << std::format("[DEBUG]: FPS: {:.1f}, avg frame time: {:.3f}", fps, avg_frame_time) << std::endl;

			start_time = end_time;
			frame_count = 0;
		}

		int width, height;
		window_get_framebuffer_size(&width, &height);

		glViewport(0, 0, width, height);
		glClear(GL_COLOR_BUFFER_BIT);

		window_swap_buffers();
		window_poll_events();

		++frame_count;
	}

	window_close();

	return 0;
}
