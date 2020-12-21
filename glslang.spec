%global commit d550bebee919179c9e332a0ab28a67f8fe3ca239
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gver .git%{shortcommit}

%global debug_package %{nil}

Name:           glslang
Version:        11.0.0
Release:        7%{?gver}%{?dist}
Summary:        OpenGL and OpenGL ES shader front end and validator

License:        BSD and GPLv3+ and ASL 2.0
URL:            https://github.com/KhronosGroup
Source0:        %url/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
Patch1:         0001-pkg-config-compatibility.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  ninja-build
BuildRequires:  spirv-tools-devel

%description
%{name} is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
%{name} is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%prep
%autosetup -p1 -n %{name}-%{commit}

%build

# We don't cmake macros here

mkdir -p build-{shared,static}

cmake3 -B shared \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_SHARED_LIBS=ON 
     

 
cmake3 -B static \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_SHARED_LIBS=OFF    

%install

%make_install -C shared

%make_install -C static


# we don't want them in here
rm -rf %{buildroot}%{_includedir}/SPIRV

cd %{buildroot}/%{_libdir}
  for lib in *.so; do
    ln -sf "${lib}" "${lib}.0"
  done


%files
%doc README.md README-spirv-remap.txt
%{_bindir}/glslangValidator
%{_bindir}/spirv-remap
%{_libdir}/libHLSL.so.0
%{_libdir}/libSPIRV.so.0
%{_libdir}/libSPVRemapper.so.0
%{_libdir}/libglslang-default-resource-limits.so.0
%{_libdir}/libglslang.so.0
%{_libdir}/libglslang.so.11
%{_libdir}/libglslang.so.11.0.0


%files devel
%{_includedir}/glslang/
%{_libdir}/libHLSL.so
%{_libdir}/libSPIRV.so
%{_libdir}/libSPVRemapper.so
%{_libdir}/libglslang-default-resource-limits.so
%{_libdir}/libglslang.so
#
%{_libdir}/libHLSL.a
%{_libdir}/libOGLCompiler.a
%{_libdir}/libOSDependent.a
%{_libdir}/libSPIRV.a
%{_libdir}/libSPVRemapper.a
%{_libdir}/libglslang.a
%{_libdir}/libGenericCodeGen.a
%{_libdir}/libMachineIndependent.a
%{_libdir}/pkgconfig/glslang.pc
%{_libdir}/pkgconfig/spirv.pc
%{_libdir}/cmake/*


%changelog
* Sun Dec 20 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 11.0.0-7
- Initial build, ready for our ffmpeg
