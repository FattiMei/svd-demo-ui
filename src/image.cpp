#include "image.h"
#include <format>
#include <cstdlib>
#include <iostream>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"


Image::Image(const std::string& filename) {
	int n_channels;
	unsigned char *data = stbi_load(filename.c_str(), &m_width, &m_height, &n_channels, 1);

	if (data == NULL) {
		std::cerr << std::format("[ERROR]: could not load {}\n", filename);
	}
	else {
		m_data.reserve(m_width * m_height);
		m_data.insert(m_data.begin(), data, data + m_width * m_height);
	}
}


Image::Image(const int width,
	     const int height,
	     const std::vector<unsigned char>& data)
	: m_width(width),
	m_height(height),
	m_data(data) {
}


int Image::get_width() const {
	return m_width;
}


int Image::get_height() const {
	return m_height;
}


unsigned char const* Image::get_data() const {
	return m_data.data();
}


Image create_random_image(const int width, const int height) {
	std::vector<unsigned char> data(width * height);

	for (size_t i = 0; i < data.size(); ++i) {
		data[i] = static_cast<unsigned char>(std::rand());
	}

	return Image(width, height, data);
}
