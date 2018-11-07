
all : dn-attachments-sync.tmp dn-projects-sync.tmp disk-space-alert.tmp
	@echo Complete

dn-attachments-sync.tmp: dn-attachments-sync.sh
	@sudo cp dn-attachments-sync.sh /usr/bin/dn-attachments-sync
	@sudo chown root:root /usr/bin/dn-attachments-sync
	@sudo chmod a+rx /usr/bin/dn-attachments-sync
	@sudo ln -f /usr/bin/dn-attachments-sync /etc/cron.hourly/
	@touch dn-attachments-sync.tmp

dn-projects-sync.tmp: dn-projects-sync.sh
	@sudo cp dn-projects-sync.sh /usr/bin/dn-projects-sync
	@sudo chown root:root /usr/bin/dn-projects-sync
	@sudo chmod a+rx /usr/bin/dn-projects-sync
	@touch dn-projects-sync.tmp

disk-space-alert.tmp: disk-space-alert.sh
	@sudo cp disk-space-alert.sh /usr/bin/disk-space-alert
	@sudo chown root:root /usr/bin/disk-space-alert
	@sudo chmod a+rx /usr/bin/disk-space-alert
	@sudo ln -f /usr/bin/disk-space-alert /etc/cron.daily/
	@touch disk-space-alert.tmp

clean:
	@rm -f *tmp
	@echo "Cleaned up"

