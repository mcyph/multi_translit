//=================================================================================//
//                       A custom, python-aware unicode string					   //
//=================================================================================//

#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <boost/python/to_python_converter.hpp>

#include "unicode/translit.h"
#include "unicode/unistr.h"
#include <stdio.h>
#include <stdlib.h>

namespace sandbox { namespace {

  class custom_string
  {
    public:
      custom_string() {}
      custom_string(UnicodeString const& value) : value_(value) {}
      UnicodeString const& value() const { return value_; }
    private:
      UnicodeString value_;
  };

  struct custom_string_to_python_str
  {
    static PyObject* convert(custom_string const& s)
    {
      return boost::python::incref(boost::python::object(s.value()).ptr());
    }
  };

  void init_module()
  {
    using namespace boost::python;

    boost::python::to_python_converter<
      custom_string,
      custom_string_to_python_str>();

    //custom_string_from_python_str();

    //def("hello", hello);
    //def("size", size);
  }
}} // namespace sandbox::<anonymous>

BOOST_PYTHON_MODULE(translit)
{
	sandbox::init_module();
}