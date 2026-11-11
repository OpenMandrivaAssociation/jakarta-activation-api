Name:		jakarta-activation-api
Version:	2.1.3
Release:	1
Summary:	Jakarta Activation API
Group:		Development/Java
License:	BSD-3-Clause
URL:		https://github.com/jakartaee/jaf-api
# Tag 2.1.3. Jakarta XML Binding API 4.0.2 depends on this coordinate.
Source0:	https://github.com/jakartaee/jaf-api/archive/refs/tags/%{version}.tar.gz#/jakarta-activation-api-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar

%description
Jakarta Activation API 2.1.3. Jakarta XML Binding API 4.0.2
depends on mvn(jakarta.activation:jakarta.activation-api).

%prep
%autosetup -n jaf-api-%{version} -p1
find . \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -delete

%build
mkdir -p classes
find api/src/main/java -name '*.java' ! -name module-info.java > sources.list
test "$(wc -l < sources.list)" -eq 28
javac --release 8 -encoding UTF-8 -Xlint:-options -d classes @sources.list
/bin/cp -a api/src/main/resources/. classes/
jar cf jakarta.activation-api.jar -C classes .
cat > jakarta.activation-api.pom <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>jakarta.activation</groupId>
  <artifactId>jakarta.activation-api</artifactId>
  <version>2.1.3</version>
  <name>Jakarta Activation API</name>
  <description>Jakarta Activation API 2.1.</description>
  <url>https://github.com/jakartaee/jaf-api</url>
  <licenses>
    <license>
      <name>BSD-3-Clause</name>
      <url>https://www.eclipse.org/org/documents/edl-v10.php</url>
    </license>
  </licenses>
</project>
EOF

%install
sysjar install --buildroot %{buildroot} \
	--artifact jakarta.activation-api.pom:jakarta.activation-api.jar \
	--file-name jakarta.activation-api \
	--filelist .mfiles

%check
JAR=%{buildroot}%{_javadir}/jakarta.activation-api.jar
test -f "$JAR"
mkdir -p check
cat > check/Smoke.java <<'END'
import jakarta.activation.MimeType;
public class Smoke {
	public static void main(String[] args) throws Exception {
		MimeType mt = new MimeType("text/plain");
		System.out.println("activation_ok " + mt.getPrimaryType() + "/" + mt.getSubType());
	}
}
END
javac --release 8 -encoding UTF-8 -Xlint:-options -cp "$JAR" -d check check/Smoke.java
java -cp "check:$JAR" Smoke > check/out.txt
cat check/out.txt
grep -F -q 'activation_ok text/plain' check/out.txt

%files -f .mfiles
%license LICENSE.md
%doc README.md NOTICE.md
