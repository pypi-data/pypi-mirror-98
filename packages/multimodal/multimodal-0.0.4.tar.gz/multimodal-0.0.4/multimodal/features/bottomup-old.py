

class ZipFeats:
    def __init__(self, path, mode) -> None:
        pass

    def __getitem__(self, name):
        pass


class COCOBottomUpFeatures:
    """
    Bottom up features for the COCO dataste
    """

    name = "coco-bottom-up"

    urls = {
        "trainval2014_36": "https://imagecaption.blob.core.windows.net/imagecaption/trainval_36.zip",  # trainval2014
        "test2015_36": "https://imagecaption.blob.core.windows.net/imagecaption/test2015_36.zip",
        "test2014_36": "https://imagecaption.blob.core.windows.net/imagecaption/test2014_36.zip",
        "trainval2014": "https://imagecaption.blob.core.windows.net/imagecaption/trainval.zip",  # trainval2014
        "test2015": "https://imagecaption.blob.core.windows.net/imagecaption/test2015.zip",
        "test2014": "https://imagecaption.blob.core.windows.net/imagecaption/test2014.zip",
    }

    tsv_paths = {
        "trainval2014_36": "trainval_36/trainval_resnet101_faster_rcnn_genome_36.tsv",
        "test2015_36": "test2015_36/test2014_resnet101_faster_rcnn_genome_36.tsv",
        "test2014_36": "test2014_36/test2014_resnet101_faster_rcnn_genome_36.tsv",
        "trainval2014": "trainval/trainval_resnet101_faster_rcnn_genome.tsv",
        "test2015": "test2015/test2014_resnet101_faster_rcnn_genome.tsv",
        "test2014": "test2014/test2014_resnet101_faster_rcnn_genome.tsv",
    }

    def __init__(self, features, dir_data=None):
        """
        features: one of [trainval2014_36, trainval2014, test2014_36, test2014, test2015-36, test2015]
        """
        self.features_name = features
        self.featsfile = None  # Lazy loading of zipfile
        dir_data = dir_data or DEFAULT_DATA_DIR
        self.dir_data = os.path.join(dir_data, "features", self.name)
        os.makedirs(self.dir_data, exist_ok=True)
        self.featspath = os.path.join(self.dir_data, features + ".zipfeat")

        # processing
        if not os.path.exists(self.featspath):
            path_download = self.download()
            print("Processing file")
            self.process_file(path_download, self.featspath)

    def download(self):
        url = self.urls[self.features_name]
        dl = SmartDL(url, self.dir_data)
        destination = dl.get_dest()
        if not os.path.exists(dl.get_dest()):
            dl.start()
        return destination

    def __getitem__(self, image_id: str):
        """
        returns dictionnary with keys:
            image_id
            image_h: int
            image_w: int
            num_boxes: int
            boxes: N, 4
            features: N, 2048
        """
        self.check_open()
        return pickle.loads(self.featsfile.read(str(image_id)))

    def check_open(self):
        if self.featsfile is None:
            self.featsfile = zipfile.ZipFile(self.featspath)

    def keys(self):
        self.check_open()
        return self.featsfile.namelist()

    def process_file(self, path_infile, outfile):
        directory = os.path.dirname(path_infile)
        tsv_path = os.path.join(directory, self.tsv_paths[self.features_name])
        try:
            if not os.path.exists(tsv_path):
                print(f"Unzipping file at {path_infile}")
                with zipfile.ZipFile(path_infile, "r") as zip_ref:
                    zip_ref.extractall(directory)
            names = set()
            num_duplicates = 0
            print(f"Processing file {tsv_path}")
        except Exception:
            os.remove(os.path.join(self.dir_data, self.features_name))
            raise
        try:
            outzip = zipfile.ZipFile(outfile, "w")
            with open(tsv_path, "r") as tsv_in_file:
                reader = csv.DictReader(
                    tsv_in_file, delimiter="\t", fieldnames=FIELDNAMES
                )
                for item in tqdm(
                    reader, total=123287, desc="Converting features to PyTables"
                ):
                    item["image_id"] = int(item["image_id"])
                    item["image_h"] = int(item["image_h"])
                    item["image_w"] = int(item["image_w"])
                    item["num_boxes"] = int(item["num_boxes"])
                    if item["image_id"] in names:
                        print(f"Duplicate {item['image_id']}")
                        num_duplicates += 1
                        continue
                    for field in ["boxes", "features"]:
                        item[field] = np.frombuffer(
                            base64.decodebytes(item[field].encode("ascii")),
                            dtype=np.float32,
                        ).reshape((item["num_boxes"], -1))
                    names.add(item["image_id"])
                    with outzip.open(str(item["image_id"]), "w") as itemfile:
                        pickle.dump(item, itemfile)
            print(f"Num duplicates : {num_duplicates}")
            outzip.close()
        except Exception:
            outzip.close()
            os.remove(outfile)
            raise
        # remove tsv
        print("Deleting tsv from disk")
        os.remove(tsv_path)




class Feature(tb.IsDescription):
    image_id = tb.Int32Col()
    image_h = tb.Int32Col()
    image_w = tb.Int32Col()
    num_boxes = tb.Int32Col()
    boxes = tb.Float32Col(shape=(36, 4))
    features = tb.Float32Col(shape=(36, 2048))


class COCOBottomUpFeaturesPyTables:
    """
    Bottom up features for the COCO dataste
    """

    name = "coco-bottom-up"

    urls = {
        "trainval2014_36": "https://imagecaption.blob.core.windows.net/imagecaption/trainval_36.zip",  # trainval2014
        "test2015_36": "https://imagecaption.blob.core.windows.net/imagecaption/test2015_36.zip",
        "test2014_36": "https://imagecaption.blob.core.windows.net/imagecaption/test2014_36.zip",
        "trainval2014": "https://imagecaption.blob.core.windows.net/imagecaption/trainval.zip",  # trainval2014
        "test2015": "https://imagecaption.blob.core.windows.net/imagecaption/test2015.zip",
        "test2014": "https://imagecaption.blob.core.windows.net/imagecaption/test2014.zip",
    }

    tsv_paths = {
        "trainval2014_36": "trainval_36/trainval_resnet101_faster_rcnn_genome_36.tsv",
        "test2015_36": "test2015_36/test2014_resnet101_faster_rcnn_genome_36.tsv",
        "test2014_36": "test2014_36/test2014_resnet101_faster_rcnn_genome_36.tsv",
        "trainval2014": [
            "trainval/karpathy_train_resnet101_faster_rcnn_genome.tsv.0", 
            "trainval/karpathy_train_resnet101_faster_rcnn_genome.tsv.1", 
            "trainval/karpathy_test_resnet101_faster_rcnn_genome.tsv",
            "trainval/karpathy_val_resnet101_faster_rcnn_genome.tsv",
        ],
        "test2015": "trainval/karpathy_test_resnet101_faster_rcnn_genome.tsv",
        "test2014": "trainval/karpathy_test_resnet101_faster_rcnn_genome.tsv",
    }

    def __init__(self, features, dir_data=None):
        """
        features: one of [trainval2014_36, trainval2014, test2014_36, test2014, test2015-36, test2015]
        """
        self.features_name = features
        self.db = None  # Lazy loading of zipfile
        dir_data = dir_data or DEFAULT_DATA_DIR
        self.dir_data = os.path.join(dir_data, "features", self.name)
        os.makedirs(self.dir_data, exist_ok=True)
        self.featspath = os.path.join(self.dir_data, features + ".tables")

        # processing
        if not os.path.exists(self.featspath):
            path_download = self.download()
            print("Processing file")
            self.process_file(path_download, self.featspath)

    def download(self):
        url = self.urls[self.features_name]
        dl = SmartDL(url, self.dir_data)
        destination = dl.get_dest()
        if not os.path.exists(dl.get_dest()):
            dl.start()
        return destination

    def __getitem__(self, image_id: str):
        self.check_open()
        data = self.db.read_where(f"image_id=={image_id}")[0]

        return {field: data[field] for field in FIELDNAMES}

    def check_open(self):
        if self.db is None:
            self.db = tb.open_file(self.featspath).root.Features

    def keys(self):
        self.check_open()
        return list(self.db.read(field="image_id"))

    def process_file(self, path_infile, outpath):
        directory = os.path.dirname(path_infile)
        tsv_path = os.path.join(directory, self.tsv_paths[self.features_name])
        try:
            if not os.path.exists(tsv_path):
                print(f"Unzipping file at {path_infile}")
                with zipfile.ZipFile(path_infile, "r") as zip_ref:
                    zip_ref.extractall(directory)
            names = set()
            num_duplicates = 0
            print(f"Processing file {tsv_path}")
        except Exception:
            os.remove(os.path.join(self.dir_data, self.features_name))
            raise
        try:
            outfile = tb.open_file(outpath, mode="w")
        except:
            os.remove(outpath)
            raise
        try:
            # root = outfile.root
            # outfile.create_group(root, "Features")
            table = outfile.create_table(outfile.root, "Features", Feature, expectedrows=123287)
            feat = table.row
            table.cols.image_id.create_index()

            # outzip = zipfile.ZipFile(outfile, "w")
            with open(tsv_path, "r") as tsv_in_file:
                reader = csv.DictReader(
                    tsv_in_file, delimiter="\t", fieldnames=FIELDNAMES
                )
                for item in tqdm(reader, total=123287, desc="Converting features to PyTables"):
                    feat["image_id"] = int(item["image_id"])
                    feat["image_h"] = int(item["image_h"])
                    feat["image_w"] = int(item["image_w"])
                    feat["num_boxes"] = int(item["num_boxes"])
                    if item["image_id"] in names:
                        print(f"Duplicate {item['image_id']}")
                        num_duplicates += 1
                        continue
                    for field in ["boxes", "features"]:
                        feat[field] = np.frombuffer(
                            base64.decodebytes(item[field].encode("ascii")),
                            dtype=np.float32,
                        ).reshape((feat["num_boxes"], -1))
                    # names.add(feat["image_id"])
                    feat.append()
            table.flush()
            print(f"Num duplicates : {num_duplicates}")
            outfile.close()
        except Exception:
            outfile.close()
            os.remove(outpath)
            raise
        # remove tsv
        print("Deleting tsv from disk")
        # os.remove(tsv_path)




class COCOBottomUpFeaturesSqlite:
    """
    Bottom up features for the COCO dataste
    """

    name = "coco-bottom-up"

    urls = {
        "trainval2014_36": "https://imagecaption.blob.core.windows.net/imagecaption/trainval_36.zip",  # trainval2014
        "test2015_36": "https://imagecaption.blob.core.windows.net/imagecaption/test2015_36.zip",
        "test2014_36": "https://imagecaption.blob.core.windows.net/imagecaption/test2014_36.zip",
        "trainval2014": "https://imagecaption.blob.core.windows.net/imagecaption/trainval.zip",  # trainval2014
        "test2015": "https://imagecaption.blob.core.windows.net/imagecaption/test2015.zip",
        "test2014": "https://imagecaption.blob.core.windows.net/imagecaption/test2014.zip",
    }

    tsv_paths = {
        "trainval2014_36": "trainval_36/trainval_resnet101_faster_rcnn_genome_36.tsv",
        "test2015_36": "test2015_36/test2014_resnet101_faster_rcnn_genome_36.tsv",
        "test2014_36": "test2014_36/test2014_resnet101_faster_rcnn_genome_36.tsv",
        "trainval2014": "trainval/trainval_resnet101_faster_rcnn_genome.tsv",
        "test2015": "test2015/test2014_resnet101_faster_rcnn_genome.tsv",
        "test2014": "test2014/test2014_resnet101_faster_rcnn_genome.tsv",
    }

    def __init__(self, features, dir_data=None):
        """
        features: one of [trainval2014_36, trainval2014, test2014_36, test2014, test2015-36, test2015]
        """
        self.features_name = features
        self.db = None  # Lazy loading of zipfile
        dir_data = dir_data or DEFAULT_DATA_DIR
        self.dir_data = os.path.join(dir_data, "features", self.name)
        os.makedirs(self.dir_data, exist_ok=True)
        self.featspath = os.path.join(self.dir_data, features + ".sqlitedict")

        # processing
        if not os.path.exists(self.featspath):
            path_download = self.download()
            print("Processing file")
            self.process_file(path_download, self.featspath)

    def download(self):
        url = self.urls[self.features_name]
        dl = SmartDL(url, self.dir_data)
        destination = dl.get_dest()
        if not os.path.exists(dl.get_dest()):
            dl.start()
        return destination

    def __getitem__(self, image_id: str):
        self.check_open()
        return self.db[image_id]

    def check_open(self):
        if self.db is None:
            self.db = sqlitedict.SqliteDict(self.featspath, flag="r")

    def keys(self):
        self.check_open()
        return self.db.keys()

    def process_file(self, path_infile, outfile):
        directory = os.path.dirname(path_infile)
        tsv_path = os.path.join(directory, self.tsv_paths[self.features_name])
        try:
            if not os.path.exists(tsv_path):
                print(f"Unzipping file at {path_infile}")
                with zipfile.ZipFile(path_infile, "r") as zip_ref:
                    zip_ref.extractall(directory)
            names = set()
            num_duplicates = 0
            print(f"Processing file {tsv_path}")
        except Exception:
            os.remove(os.path.join(self.dir_data, self.features_name))
            raise

        try:
            outdb = sqlitedict.SqliteDict(outfile)
        except Exception:
            os.remove(outfile)
            raise
        try:
            # outzip = zipfile.ZipFile(outfile, "w")
            with open(tsv_path, "r") as tsv_in_file:
                reader = csv.DictReader(
                    tsv_in_file, delimiter="\t", fieldnames=FIELDNAMES
                )
                for item in tqdm(
                    reader, total=123287, desc="Converting features to PyTables"
                ):
                    item["image_id"] = int(item["image_id"])
                    item["image_h"] = int(item["image_h"])
                    item["image_w"] = int(item["image_w"])
                    item["num_boxes"] = int(item["num_boxes"])
                    if item["image_id"] in names:
                        print(f"Duplicate {item['image_id']}")
                        num_duplicates += 1
                        continue
                    for field in ["boxes", "features"]:
                        item[field] = np.frombuffer(
                            base64.decodebytes(item[field].encode("ascii")),
                            dtype=np.float32,
                        ).reshape((item["num_boxes"], -1))
                    names.add(item["image_id"])
                    outdb[str(item["image_id"])] = item
            print(f"Num duplicates : {num_duplicates}")
            outdb.commit()
        except Exception:
            outdb.close()
            os.remove(outfile)
            raise
        # remove tsv
        print("Deleting tsv from disk")
        os.remove(tsv_path)


try:
    from lsm import LSM
except:
    pass


class COCOBottomUpFeaturesLSM:
    """
    Bottom up features for the COCO dataste
    """

    name = "coco-bottom-up"

    urls = {
        "trainval2014_36": "https://imagecaption.blob.core.windows.net/imagecaption/trainval_36.zip",  # trainval2014
        "test2015_36": "https://imagecaption.blob.core.windows.net/imagecaption/test2015_36.zip",
        "test2014_36": "https://imagecaption.blob.core.windows.net/imagecaption/test2014_36.zip",
        "trainval2014": "https://imagecaption.blob.core.windows.net/imagecaption/trainval.zip",  # trainval2014
        "test2015": "https://imagecaption.blob.core.windows.net/imagecaption/test2015.zip",
        "test2014": "https://imagecaption.blob.core.windows.net/imagecaption/test2014.zip",
    }

    tsv_paths = {
        "trainval2014_36": "trainval_36/trainval_resnet101_faster_rcnn_genome_36.tsv",
        "test2015_36": "test2015_36/test2014_resnet101_faster_rcnn_genome_36.tsv",
        "test2014_36": "test2014_36/test2014_resnet101_faster_rcnn_genome_36.tsv",
        "trainval2014": "trainval/trainval_resnet101_faster_rcnn_genome.tsv",
        "test2015": "test2015/test2014_resnet101_faster_rcnn_genome.tsv",
        "test2014": "test2014/test2014_resnet101_faster_rcnn_genome.tsv",
    }

    def __init__(self, features, dir_data=None):
        """
        features: one of [trainval2014_36, trainval2014, test2014_36, test2014, test2015-36, test2015]
        """
        self.features_name = features
        self.db = None  # Lazy loading of zipfile
        dir_data = dir_data or DEFAULT_DATA_DIR
        self.dir_data = os.path.join(dir_data, "features", self.name)
        os.makedirs(self.dir_data, exist_ok=True)
        self.featspath = os.path.join(self.dir_data, features + ".lsmdb")

        # processing
        if not os.path.exists(self.featspath):
            path_download = self.download()
            print("Processing file")
            self.process_file(path_download, self.featspath)

    def download(self):
        url = self.urls[self.features_name]
        dl = SmartDL(url, self.dir_data)
        destination = dl.get_dest()
        if not os.path.exists(dl.get_dest()):
            dl.start()
        return destination

    def __getitem__(self, image_id: str):
        self.check_open()
        return self.db[image_id]

    def check_open(self):
        if self.db is None:
            self.db = LSM(self.featspath)

    def keys(self):
        self.check_open()
        return self.db.keys()

    def process_file(self, path_infile, outfile):
        directory = os.path.dirname(path_infile)
        tsv_path = os.path.join(directory, self.tsv_paths[self.features_name])
        try:
            if not os.path.exists(tsv_path):
                print(f"Unzipping file at {path_infile}")
                with zipfile.ZipFile(path_infile, "r") as zip_ref:
                    zip_ref.extractall(directory)
            names = set()
            num_duplicates = 0
            print(f"Processing file {tsv_path}")
        except Exception:
            os.remove(os.path.join(self.dir_data, self.features_name))
            raise
        try:
            outdb = LSM(outfile)
        except:
            os.remove(outfile)
            raise
        try:
            # outzip = zipfile.ZipFile(outfile, "w")
            with open(tsv_path, "r") as tsv_in_file:
                reader = csv.DictReader(
                    tsv_in_file, delimiter="\t", fieldnames=FIELDNAMES
                )
                for item in tqdm(
                    reader, total=123287, desc="Converting features to PyTables"
                ):
                    item["image_id"] = int(item["image_id"])
                    item["image_h"] = int(item["image_h"])
                    item["image_w"] = int(item["image_w"])
                    item["num_boxes"] = int(item["num_boxes"])
                    if item["image_id"] in names:
                        print(f"Duplicate {item['image_id']}")
                        num_duplicates += 1
                        continue
                    for field in ["boxes", "features"]:
                        item[field] = np.frombuffer(
                            base64.decodebytes(item[field].encode("ascii")),
                            dtype=np.float32,
                        ).reshape((item["num_boxes"], -1))
                    names.add(item["image_id"])
                    outdb[str(item["image_id"])] = item
            print(f"Num duplicates : {num_duplicates}")
            outdb.commit()
        except Exception:
            outdb.close()
            os.remove(outfile)
            raise
        # remove tsv
        print("Deleting tsv from disk")
        os.remove(tsv_path)

