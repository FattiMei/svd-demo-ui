#include "image.h"
#include <cstdlib>


// TODO: add stb_image image loading and processing
Image::Image(const std::string& /* filename */) {

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


Image create_random_image(const int width, const int height) {
	std::vector<unsigned char> data(width * height);

	for (size_t i = 0; i < data.size(); ++i) {
		data[i] = static_cast<unsigned char>(std::rand());
	}

	return Image(width, height, data);
}
