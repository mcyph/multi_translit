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

  class MyUniString
  {
    public:
      MyUniString() {}
      MyUniString(UnicodeString const& value) : value_(value) {}
	  std::string const value() const
	  {
		  char Out[32768];
		  Out[value_.extract(0, 32768, Out, "utf-8")]=0;
		  //printf("Out: ", Out);

		  std::string ReturnData(Out);
		  //printf("ReturnData: ", ReturnData);
		  return ReturnData;
	  }
    private:
      UnicodeString value_;
  };

  struct MyUniString_to_python_str
  {
    static PyObject* convert(MyUniString const& s)
    {
      return boost::python::incref(boost::python::object(s.value()).ptr());
    }
  };

  void init_module()
  {
    using namespace boost::python;

    boost::python::to_python_converter<
      MyUniString,
      MyUniString_to_python_str>();

    //MyUniString_from_python_str();

    //def("hello", hello);
    //def("size", size);
  }
}} // namespace sandbox::<anonymous>

