#include "version.h"
#include <format>


Version::Version(unsigned int major, unsigned int minor) : m_major(major), m_minor(minor) {
}


unsigned int Version::get_major() const {
	return m_major;
}


unsigned int Version::get_minor() const {
	return m_minor;
}


std::string Version::to_string() const {
	return std::format("{}.{}", m_major, m_minor);
}
