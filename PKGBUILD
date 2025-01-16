pkgname=pawfetch
pkgver=0.1
pkgrel=1
pkgdesc="the cutest fetch, featuring (trans)puppies"
arch=('any')
url="https://github.com/jade-gay/pawfetch"
license=('GPL')
depends=('python' 'python-psutil')
source=("git+https://github.com/jade-gay/pawfetch.git")
sha256sums=('SKIP')

package() {
  cd "$srcdir/$pkgname"
  
  install -Dm755 pawfetch.py "$pkgdir/usr/bin/pawfetch"
}
