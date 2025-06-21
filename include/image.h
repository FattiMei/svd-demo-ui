#ifndef __IMAGE_H__
#define __IMAGE_H__


#include <string>
#include <vector>


class Image {
	public:
		Image(const std::string& filename);
		Image(const int width,
	              const int height,
		      const std::vector<unsigned char>& data);

		int get_width() const;
		int get_height() const;
		unsigned char const* get_data() const;

	private:
		int m_width, m_height;
		std::vector<unsigned char> m_data;
};


Image create_random_image(const int width, const int height);


#endif // __IMAGE_H__
