#include <format>
#include <vector>
#include <iomanip>
#include <iostream>
#include <GLFW/glfw3.h>


const std::vector<std::pair<int,int>> window_hints = {
	{GLFW_RESIZABLE                 , GLFW_TRUE                 },
	{GLFW_VISIBLE                   , GLFW_TRUE                 },
	{GLFW_DECORATED                 , GLFW_TRUE                 },
	{GLFW_FOCUSED                   , GLFW_TRUE                 },
	{GLFW_AUTO_ICONIFY              , GLFW_TRUE                 },
	{GLFW_FLOATING                  , GLFW_FALSE                },
	{GLFW_MAXIMIZED                 , GLFW_FALSE                },
	{GLFW_CENTER_CURSOR             , GLFW_TRUE                 },
	{GLFW_TRANSPARENT_FRAMEBUFFER   , GLFW_FALSE                },
	{GLFW_FOCUS_ON_SHOW             , GLFW_TRUE                 },
	{GLFW_SCALE_TO_MONITOR          , GLFW_FALSE                },
	{GLFW_RED_BITS                  , 8                         },
	{GLFW_GREEN_BITS                , 8                         },
	{GLFW_BLUE_BITS                 , 8                         },
	{GLFW_ALPHA_BITS                , 8                         },
	{GLFW_DEPTH_BITS                , 24                        },
	{GLFW_STENCIL_BITS              , 8                         },
	{GLFW_ACCUM_RED_BITS            , 0                         },
	{GLFW_ACCUM_GREEN_BITS          , 0                         },
	{GLFW_ACCUM_BLUE_BITS           , 0                         },
	{GLFW_ACCUM_ALPHA_BITS          , 0                         },
	{GLFW_AUX_BUFFERS               , 0                         },
	{GLFW_SAMPLES                   , 0                         },
	{GLFW_REFRESH_RATE              , GLFW_DONT_CARE            },
	{GLFW_STEREO                    , GLFW_FALSE                },
	{GLFW_SRGB_CAPABLE              , GLFW_FALSE                },
	{GLFW_DOUBLEBUFFER              , GLFW_TRUE                 },
	{GLFW_CONTEXT_ROBUSTNESS        , GLFW_NO_ROBUSTNESS        },
	{GLFW_CONTEXT_RELEASE_BEHAVIOR  , GLFW_ANY_RELEASE_BEHAVIOR },
	{GLFW_OPENGL_FORWARD_COMPAT     , GLFW_FALSE                },
	{GLFW_OPENGL_DEBUG_CONTEXT      , GLFW_FALSE                },
	{GLFW_OPENGL_PROFILE            , GLFW_OPENGL_ANY_PROFILE   },
#ifdef USE_OPENGL_ES2
	{GLFW_CLIENT_API		, GLFW_OPENGL_ES_API	    },
	{GLFW_CONTEXT_CREATION_API	, GLFW_EGL_CONTEXT_API	    },
	{GLFW_CONTEXT_VERSION_MAJOR	, 2			    },
	{GLFW_CONTEXT_VERSION_MINOR	, 0			    }
#else
	{GLFW_CLIENT_API                , GLFW_OPENGL_API           },
	{GLFW_CONTEXT_CREATION_API      , GLFW_NATIVE_CONTEXT_API   },
	{GLFW_CONTEXT_VERSION_MAJOR     , 4                         },
	{GLFW_CONTEXT_VERSION_MINOR     , 3                         }
#endif
};


void error_callback(int error, const char* description) {
	std::cerr << std::format("[ERROR]: GLFW error (code {}) - {}", error, description) << std::endl;
}


static void key_callback(GLFWwindow* window, int key, int /* scancode */, int action, int /* mods */) {
	if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
		glfwSetWindowShouldClose(window, GLFW_TRUE);
	}
}


int main(int argc, char* argv[]) {
	const char* image_name = "resources/einstein.jpeg";
	if (argc < 2) {
		std::cerr << "[INFO]: no image provided, loading default image" << std::endl;
	}
	else {
		image_name = argv[1];
	}

	std::cerr << std::format("[INFO]: loading \"{}\"", image_name) << std::endl;


	glfwSetErrorCallback(error_callback);

	if (not glfwInit()) {
		std::cerr << "[ERROR]: GLFW initialization failed" << std::endl;
		return 1;
	}

	for (const auto& [hint, value] : window_hints) {
		glfwWindowHint(hint, value);
	}

	// the size of the window will have to be compatible with the layout of the images
	GLFWwindow* window = glfwCreateWindow(600, 600, "SVD demo", NULL, NULL);
	if (window == NULL) {
		glfwTerminate();
		return 2;
	}

	glfwSetKeyCallback(window, key_callback);
	glfwMakeContextCurrent(window);

	// this could be unnecessay if OpenGL has been linked at compile time, right?
	// gladLoadGL(glfwGetProcAddress);

	// ---------------------------- interactivity section ------------------------
	auto start_time = glfwGetTime();
	size_t frame_count = 0;

	while (!glfwWindowShouldClose(window)) {
		// frame time logic, just to have a measure of the smoothness of the UI
		const auto end_time = glfwGetTime();
		const auto delta_t = end_time - start_time;

		if (delta_t > 1.0) {
			const auto fps = static_cast<double>(frame_count) / delta_t;
			const auto avg_frame_time = delta_t / frame_count;

			std::cout
				<< "FPS: " << std::setprecision(3) << fps
				<< ", "
				<< "avg frame time: " << avg_frame_time
				<< std::endl;


			start_time = end_time;
			frame_count = 0;
		}

		int width, height;
		glfwGetFramebufferSize(window, &width, &height);

		glViewport(0, 0, width, height);
		glClear(GL_COLOR_BUFFER_BIT);

		glfwSwapBuffers(window);
		glfwPollEvents();

		++frame_count;
	}

	glfwDestroyWindow(window);
	glfwTerminate();

	return 0;
}

