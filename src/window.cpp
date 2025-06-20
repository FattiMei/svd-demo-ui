#include <cstdio>
#include "window.h"


static const int default_window_hints[][2] = {
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


static GLFWwindow* window = NULL;


static void error_callback(int error, const char* description) {
	fprintf(stderr, "[GLFW ERROR - code %d]: %s\n", error, description);
}


static void window_set_hints(const int n, const int hints[][2]) {
	for (int i = 0; i < n; ++i) {
		glfwWindowHint(hints[i][0], hints[i][1]);
	}
}


int window_init(const char* title, const int width, const int height) {
	glfwSetErrorCallback(error_callback);

	if (glfwInit() == 0) {
		return 1;
	}

	window_set_hints(sizeof(default_window_hints) / (2 * sizeof(int)),
			 default_window_hints);

	window = glfwCreateWindow(width, height, title, NULL, NULL);
	if (window == NULL) {
		glfwTerminate();
		return 2;
	}

	glfwMakeContextCurrent(window);

	// this is unnecessay if the program links with OpenGL
	// it has not been tested for OpenGL_ES contexts (TODO)
	// gladLoadGL(glfwGetProcAddress);

	return 0;
}


void window_set_key_callback(key_callback_t cb) {
	glfwSetKeyCallback(window, cb);
}


void window_set_mouse_callback(mouse_callback_t cb) {
	glfwSetMouseButtonCallback(window, cb);
}


void window_set_resize_callback(resize_callback_t cb) {
	glfwSetFramebufferSizeCallback(window, cb);
}


void window_get_framebuffer_size(int* width, int* height) {
	glfwGetFramebufferSize(window, width, height);
}


char* window_get_opengl_version() {
	return (char*) glGetString(GL_VERSION);
}


int window_should_close() {
	return glfwWindowShouldClose(window);
}

void window_swap_buffers() {
	glfwSwapBuffers(window);
}


void window_poll_events() {
	glfwPollEvents();
}


void window_close() {
	glfwDestroyWindow(window);
	glfwTerminate();
}


void exit_on_escape_callback(GLFWwindow* window,
		             int key,
			     int /* scancode */,
			     int action,
			     int /* mods */) {
	if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
		glfwSetWindowShouldClose(window, GLFW_TRUE);
	}
}
