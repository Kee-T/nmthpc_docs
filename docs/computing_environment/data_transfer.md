# Transferring Data

This guide covers methods for transferring data between your local system and the NMTHPC cluster.

## Before You Transfer

### Planning Your Transfer

Consider:

- **Data size**: Small files (< 1 GB), medium (1-100 GB), or large (> 100 GB)
- **Number of files**: Few large files vs. many small files
- **Frequency**: One-time transfer vs. regular synchronization
- **Location**: Where you're transferring from (on-campus, off-campus, another HPC center)

### Destination Filesystems

Choose the appropriate destination:

- **Home directory** (`/home/username`): Small datasets, code, scripts
- **{{nmthpc_filesystem_1}}**: Active project data, large datasets
- **{{nmthpc_filesystem_2}}**: Long-term storage, archival data

See [Nodes and Filesystems](nodes_filesystems.md) for more information.

## Command-Line Tools

### SCP (Secure Copy)

Best for: Small to medium-sized files, simple one-time transfers

**Copy file TO NMTHPC**:
```bash
$ scp localfile.txt username@hpc.nmt.edu:~/
```

**Copy file FROM NMTHPC**:
```bash
$ scp username@hpc.nmt.edu:~/remotefile.txt ./
```

**Copy directory recursively**:
```bash
$ scp -r local_directory username@hpc.nmt.edu:~/destination/
```

**Copy multiple files**:
```bash
$ scp file1.txt file2.txt username@hpc.nmt.edu:~/data/
```

### Rsync (Recommended for Most Transfers)

Best for: Synchronizing directories, resumable transfers, large datasets

**Basic rsync to NMTHPC**:
```bash
$ rsync -avzP local_directory username@hpc.nmt.edu:~/remote_directory/
```

**Flags explained**:

- `-a`: Archive mode (preserves permissions, timestamps)
- `-v`: Verbose output
- `-z`: Compress during transfer
- `-P`: Show progress and allow resuming

**Rsync from NMTHPC**:
```bash
$ rsync -avzP username@hpc.nmt.edu:~/remote_directory ./local_directory/
```

**Dry run** (see what would be transferred):
```bash
$ rsync -avzPn local_directory username@hpc.nmt.edu:~/remote_directory/
```

**Exclude files**:
```bash
$ rsync -avzP --exclude='*.log' --exclude='tmp/' local_dir username@hpc.nmt.edu:~/
```

**Delete files on destination** (use carefully):
```bash
$ rsync -avzP --delete local_directory username@hpc.nmt.edu:~/remote_directory/
```

```{tip}
Rsync only transfers changed files, making it ideal for synchronizing directories and resuming interrupted transfers.
```

### SFTP (Interactive File Transfer)

Best for: Interactive browsing and selective file transfers

**Start SFTP session**:
```bash
$ sftp username@hpc.nmt.edu
```

**Common SFTP commands**:
```bash
sftp> ls                  # List remote files
sftp> lls                 # List local files
sftp> cd remote_dir       # Change remote directory
sftp> lcd local_dir       # Change local directory
sftp> get remotefile.txt  # Download file
sftp> put localfile.txt   # Upload file
sftp> get -r directory    # Download directory
sftp> put -r directory    # Upload directory
sftp> exit                # Exit SFTP
```

## Graphical Tools

### FileZilla (Cross-Platform)

**Setup**:

1. Download from [filezilla-project.org](https://filezilla-project.org/)
2. Open FileZilla and create new site
3. Configure connection:
   - Protocol: SFTP
   - Host: `hpc.nmt.edu`
   - Port: 22
   - User: your username
   - Password: your password (or use SSH key)

**Usage**: Drag and drop files between local (left) and remote (right) panels

### WinSCP (Windows)

**Setup**:

1. Download from [winscp.net](https://winscp.net/)
2. Create new session
3. Enter connection details:
   - Host name: `hpc.nmt.edu`
   - Port: 22
   - Username and password

**Usage**: Drag and drop interface similar to Windows Explorer

### Cyberduck (macOS/Windows)

**Setup**:

1. Download from [cyberduck.io](https://cyberduck.io/)
2. Click "Open Connection"
3. Select SFTP protocol
4. Enter `hpc.nmt.edu` and credentials

## Large Data Transfers

### Globus

Best for: Very large datasets (> 100 GB), reliable transfers with automatic retry

Globus provides fast, reliable data transfer between institutions.

**Setup** (if available):

1. Visit [globus.org](https://www.globus.org/) and sign in
2. Search for NMT HPC endpoint
3. Set up transfers through web interface

```{note}
Check with HPC support (<hpc@nmthpc.atlassian.net>) for Globus availability and endpoint name.
```

### Tar and Compress Before Transfer

For many small files, compress into a single archive first:

**Create compressed archive**:
```bash
$ tar -czf mydata.tar.gz my_directory/
```

**Transfer archive**:
```bash
$ rsync -avP mydata.tar.gz username@hpc.nmt.edu:~/
```

**Extract on NMTHPC**:
```bash
$ tar -xzf mydata.tar.gz
```

```{tip}
Transferring a single compressed archive is much faster than transferring thousands of small files individually.
```

## Transfer Best Practices

### Optimize Transfer Speed

1. **Compress data**: Use `-z` with rsync or create tar.gz archives
2. **Use multiple connections**: Some tools support parallel transfers
3. **On-campus transfers**: Faster when on NMT network
4. **Off-campus**: Use VPN for security and potentially better routing
5. **Avoid peak hours**: Large transfers are faster during off-peak times

### Many Small Files

For directories with many small files:

**Option 1: Create archive first**:
```bash
$ tar -czf archive.tar.gz directory/
$ rsync -avP archive.tar.gz username@hpc.nmt.edu:~/
```

**Option 2: Use rsync with appropriate options**:
```bash
$ rsync -avzP --info=progress2 directory/ username@hpc.nmt.edu:~/directory/
```

### Verification

**Verify transfer with checksums**:

Local system:
```bash
$ md5sum largefile.dat > largefile.md5
```

After transfer to NMTHPC:
```bash
$ md5sum -c largefile.md5
```

**Compare directory sizes**:
```bash
$ du -sh directory
```

## Transferring from Other HPC Systems

### Direct Transfer Between HPC Systems

**From NMTHPC to another HPC**:
```bash
# On NMTHPC
$ scp -r data/ username@other-hpc.edu:~/destination/
```

**From another HPC to NMTHPC**:
```bash
# On the other HPC system
$ scp -r data/ username@hpc.nmt.edu:~/destination/
```

**Using Globus**: Often the best option for HPC-to-HPC transfers

## Troubleshooting

### Transfer is Slow

- Check network connection quality
- Try compression: `rsync -avzP`
- Consider transferring during off-peak hours
- For large datasets, investigate Globus
- Verify you're not transferring unnecessary files

### Connection Interrupted

Use `rsync` instead of `scp` - it can resume:
```bash
$ rsync -avzP --partial directory/ username@hpc.nmt.edu:~/directory/
```

### Permission Denied

- Verify destination directory exists
- Check write permissions on destination
- Ensure you have quota space available:
  ```bash
  $ quota -s
  ```

### Too Many Small Files

- Create tar archive first
- Use `rsync` with `--info=progress2` for better progress reporting
- Consider parallel transfer tools for very large numbers of files

## Automated Transfers

### Using SSH Keys for Automation

Set up SSH keys to avoid entering passwords:

```bash
# Generate key (if you haven't already)
$ ssh-keygen -t ed25519

# Copy to NMTHPC
$ ssh-copy-id username@hpc.nmt.edu
```

### Automated Rsync with Cron

**Example sync script** (`sync_to_nmthpc.sh`):
```bash
#!/bin/bash
rsync -avzP ~/local_data/ username@hpc.nmt.edu:~/remote_data/
```

**Schedule with cron**:
```bash
$ crontab -e
# Add line to run daily at 2 AM:
0 2 * * * /path/to/sync_to_nmthpc.sh
```

## Bandwidth Considerations

### Estimating Transfer Time

**Rough estimates**:

- On-campus (1 Gbps): ~100 MB/s
- Off-campus (typical): 10-50 MB/s
- Calculate: `File size (GB) / Speed (GB/s) = Time (seconds)`

**Example**: 100 GB at 50 MB/s = 100,000 MB / 50 MB/s = 2,000 seconds ≈ 33 minutes

### Large Dataset Strategies

For TB-scale data:

1. **Ship hard drives** for initial transfer (contact HPC support)
2. **Use Globus** for automated, managed transfers
3. **Transfer incrementally** rather than all at once
4. **Compress** when possible
5. **Clean up** local copies after verification

## Summary of Methods

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| `scp` | Small files, quick transfers | Simple, universally available | No resume, not for large datasets |
| `rsync` | Regular syncing, large directories | Resumable, efficient | Slightly more complex |
| `sftp` | Interactive browsing | User-friendly | Manual process |
| FileZilla/WinSCP | GUI users | Easy to use | Not for automation |
| Globus | Very large datasets | Reliable, managed | Setup required |

## Questions?

For questions about data transfer or issues with file transfers, contact <hpc@nmthpc.atlassian.net>.
