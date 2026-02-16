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
$ scp localfile.txt username@nmthpc.id.nmt.edu:~/
```

**Copy file FROM NMTHPC**:
```bash
$ scp username@nmthpc.id.nmt.edu:~/remotefile.txt ./
```

**Copy directory recursively**:
```bash
$ scp -r local_directory username@nmthpc.id.nmt.edu:~/destination/
```

**Copy multiple files**:
```bash
$ scp file1.txt file2.txt username@nmthpc.id.nmt.edu:~/data/
```

### Rsync (Recommended for Most Transfers)

Best for: Synchronizing directories, resumable transfers, large datasets

**Basic rsync to NMTHPC**:
```bash
$ rsync -avzP local_directory username@nmthpc.id.nmt.edu:~/remote_directory/
```

**Flags explained**:

- `-a`: Archive mode (preserves permissions, timestamps)
- `-v`: Verbose output
- `-z`: Compress during transfer
- `-P`: Show progress and allow resuming

**Rsync from NMTHPC**:
```bash
$ rsync -avzP username@nmthpc.id.nmt.edu:~/remote_directory ./local_directory/
```

**Dry run** (see what would be transferred):
```bash
$ rsync -avzPn local_directory username@nmthpc.id.nmt.edu:~/remote_directory/
```

**Exclude files**:
```bash
$ rsync -avzP --exclude='*.log' --exclude='tmp/' local_dir username@nmthpc.id.nmt.edu:~/
```

**Delete files on destination** (use carefully):
```bash
$ rsync -avzP --delete local_directory username@nmthpc.id.nmt.edu:~/remote_directory/
```

```{tip}
Rsync only transfers changed files, making it ideal for synchronizing directories and resuming interrupted transfers.
```

### Tar and Compress Before Transfer

For many small files, compress into a single archive first:

**Create compressed archive**:
```bash
$ tar -czf mydata.tar.gz my_directory/
```

**Transfer archive**:
```bash
$ rsync -avP mydata.tar.gz username@nmthpc.id.nmt.edu:~/
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
$ rsync -avP archive.tar.gz username@nmthpc.id.nmt.edu:~/
```

**Option 2: Use rsync with appropriate options**:
```bash
$ rsync -avzP --info=progress2 directory/ username@nmthpc.id.nmt.edu:~/directory/
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
$ scp -r data/ username@nmthpc.id.nmt.edu:~/destination/
```

## Troubleshooting

### Transfer is Slow


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
$ ssh-copy-id username@nmthpc.id.nmt.edu
```

## Questions?

For questions about data transfer or issues with file transfers, contact <hpc@nmthpc.atlassian.net>.

