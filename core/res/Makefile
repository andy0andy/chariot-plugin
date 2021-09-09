# 用于创建插件压缩包和编译镜像


VERSION?=$(shell grep '^version: ' plugin.spec.yaml | sed 's/version: //')
NAME?=$(shell grep '^name: ' plugin.spec.yaml | sed 's/name: //')
VENDOR?=$(shell grep '^vendor: ' plugin.spec.yaml | sed 's/vendor: //')
CWD?=$(shell basename $(PWD))
_NAME?=$(shell echo $(NAME) | awk '{ print toupper(substr($$0,1,1)) tolower(substr($$0,2)) }')
PKG=$(VENDOR)-$(NAME)-$(VERSION).tar.gz

# 基于时间戳的随机字符串
TIMESTAMP=$(date +%s%N | md5sum | head -c 10)


.DEFAULT_GOAL := defaultsdk


default: image tarball

tarball:
	$(info [$(YELLOW)*$(NORMAL)] Creating plugin tarball)
	rm -rf build
	rm -rf $(PKG)
	tar -cvzf $(PKG) --exclude=$(PKG) --exclude=tests --exclude=run.sh *

image:
	$(info [$(YELLOW)*$(NORMAL)] Building plugin image)
	docker build --pull -t $(VENDOR)/$(NAME):$(VERSION) .
	docker tag $(VENDOR)/$(NAME):$(VERSION) $(VENDOR)/$(NAME):latest



