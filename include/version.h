#ifndef __VERSION_H__
#define __VERSION_H__


#include <string>
#include <format>


// it is used to model the OpenGL context version
class Version {
	public:
		Version(unsigned int major, unsigned int minor = 0);

		unsigned int get_major() const;
		unsigned int get_minor() const;

		std::string to_string() const;

	private:
		const unsigned int m_major, m_minor;
};


#endif // __VERSION_H__
