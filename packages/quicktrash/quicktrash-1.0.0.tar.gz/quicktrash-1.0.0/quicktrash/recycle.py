import typing
import os, shutil, filelock, pathlib, sys

class Trashlet:
    trashletdir:str

    def __init__(self, trashletdir:str):
        self.trashletdir = trashletdir
    
    def recycle(self, filepath:str) -> str:
        filepath = os.path.abspath(filepath)

        if not os.path.exists(filepath):
            return None

        parent, name = os.path.split(filepath)

        virtualparent = os.path.join(self.trashletdir, parent.strip(os.sep))
        virtualpath = os.path.join(virtualparent, name)

        if not os.path.exists(virtualparent):
            os.makedirs(virtualparent)
        elif os.path.exists(virtualpath):
            raise FileExistsError()

        if os.path.isdir(filepath):
            shutil.move(filepath, virtualpath)
        else:
            os.rename(filepath, virtualpath)
        
        return virtualpath

class Trash:
    trashdir:str

    def __init__(self, trashdir:str):
        self.trashdir = trashdir

    @property
    def _lockfile(self):
        return os.path.join(self.trashdir, "lockfile")
    
    @property
    def _leaderfile(self):
        return os.path.join(self.trashdir, "leader")

    @property
    def _lock(self):
        try:
            os.makedirs(self.trashdir)
        except FileExistsError:
            pass
        
        pathlib.Path(self._lockfile).touch()
        return filelock.FileLock(self._lockfile)

    @property
    def _next_directory(self):
        with self._lock:
            index:int
            read:bool = False
            if os.path.exists(self._leaderfile):
                try:
                    with open(self._leaderfile, "r") as stream:
                        content:str = stream.read().strip()
                        index = int(content, 16) + 1

                    read = True
                except ValueError:
                    pass
            
            if read:
                while True:
                    destfolder = os.path.join(self.trashdir, hex(index))
                    
                    if os.path.exists(destfolder):
                        index += 1
                    else:
                        break
            else:
                highest:int = 0

                filelist:list = os.listdir(self.trashdir)

                for metafile in (self._lockfile, self._leaderfile):
                    if metafile in filelist:
                        filelist.remove(metafile)

                for parentpath, name in map(os.path.split, filelist):
                    try:
                        val = int(name, 16)

                        if val > highest:
                            highest = val
                    except ValueError:
                        continue
                
                index = highest + 1
                
                destfolder = os.path.join(self.trashdir, hex(index))
                
            with open(self._leaderfile, "w") as stream:
                stream.write(hex(index))
        
            return destfolder
    
    def __next__(self) -> Trashlet:
        return Trashlet(self._next_directory)

    def __enter__(self) -> Trashlet:
        return next(self)
    
    def __exit__(self, *args, **kwargs):
        ...