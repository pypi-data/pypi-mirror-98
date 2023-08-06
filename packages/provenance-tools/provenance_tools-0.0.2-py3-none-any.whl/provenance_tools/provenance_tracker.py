import git, hashlib, inspect, warnings, os, argparse, pdb
from argparse import ArgumentParser
import xml.etree.ElementTree as et
import platform, datetime

def insert_xml_tree(parent_el, child_el, sha1=None):
    """Recurvsive function meant to facilitate the insertion of a file's
    provenance info into another provenenance info tree.

    Parameters
    ----------
    parent_el : xml.etree.Element
        The parent element into which to insert the child element information

    child_el : xml.etree.Element
        The child element will be inserted as a sub-element into the parent
        element. If the child element itself has children, they will be
        recursively added to the tree.

    sha1 : string, optional
        The sha1 code, computed at runtime, of the dependency file. If
        supplied, this function will check whether the runtime sha1 code
        matches the stored sha1 code. If not, a warning message is issued.
    """
    tmp_el = et.SubElement(parent_el, child_el.tag, child_el.attrib)
    tmp_el.text = child_el.text

    if sha1 is not None:
        if child_el.tag == 'sha1':
            if sha1 != child_el.text:
                warnings.warn("sha1 mismatch in provenance tree! {} vs {}".\
                              format(sha1, child_el.text))

    for el in list(child_el):
        insert_xml_tree(tmp_el, el)

def insert_dependency_file_info(parent_el, file_name):
    """This function will compute run-time sha1 hash for the specified file,
    and it will check to see if a corresponding provenance info file exits. If
    it does, it will be read in. This information will be inserted under
    'parent_el'.
    """
    sha1 = et.SubElement(parent_el, 'sha1')
    sha1.text = hashlib.sha1(open(file_name, 'rb').read()).hexdigest()

    fname = et.SubElement(parent_el, 'file_name')
    fname.text = file_name

    # Check to see if this file has a corresponding provenance file. If it does,
    # read it in and include its info
    p_info_file = file_name + '.provenance_info.xml'
    if os.path.isfile(p_info_file):
        tmp_tree = et.parse(p_info_file)
        insert_xml_tree(parent_el, tmp_tree.getroot(), sha1.text)

def write_provenance_data(file_names, write_generator_info=True,
                          generator_args=None, aux_file_deps=None, desc=None,
                          generator_file_name=None):
    """Generate provenace information for a data file. This function will
    produce provenance information for 'file_name' and will store that info
    in 'file_name.provenance_info.xml'.

    Parameters
    ----------
    file_names : str or list of strings
        The name(s) of the file for which to generate provenance info.

    write_generator_info : boolean, optional
        The common use case is for this function to be invoked within some
        module that produces a data file for which we want to generate
        provenance info. By default, information about the generating
        file will be stored. This includes the file's name
        (/provenance_info/generator_info/generator_file) and the repository
        commit version (/provenance_info/generator_info/commit). This function
        assumes that the generating file is under git version control. Note that
        if this function is invoked in a repository that is not up-to-date, an
        error is generated.

    generator_args : argparse.Namespace, optional
        If any arguments are passed to the generating file, they should passed
        to this function to be recorded. It is assumed that argument parsing is
        managed with python's argparse.ArgumentParser. Each argument will be
        stored as is. Also, each argument will be tested to see if it is an
        input file. If so, the sha1 hash code will be generated for that file
        and stored with element name corresponding to flag name followed by
        '_sha1'. The args are stored in
        /provenance_info/generator_info/arg_info.

    aux_file_deps : dict, optional
        A dictionary containing file variable names from the calling script
        (the dictionary keys) and associated file name paths (the dictionary
        values). Use this record information about files that may be hard-coded
        in the generating file (i.e. that are not read in as arguments). For
        each file in the dictionary, a check will be permormed to see if there
        is associated provenance information (with the original file name plus
        the extension '.provenance_info.xml'). If the provenance information
        exists, it will be read in and appended to the current file's provenance
        information with tag '<key_val>_provenenance_info'.

    desc : str, optional
        A free-form string description that provides information about the
        file's contents.

    generator_file_name : str, optional
        The name of the generating file (e.g. file name of the script that was
        used to produce the data file). Specifying this variable is only
        necessary if this function is being invoked from within R.
    """
    if type(file_names) != list:
        file_names = [file_names]

    for file_name in file_names:
        if not os.path.isfile(file_name):
            raise ValueError('File does not exist')
    
        p_info = et.Element('provenance_info')
        sha1 = et.SubElement(p_info, 'sha1')
        sha1.text = hashlib.sha1(open(file_name, 'rb').read()).hexdigest()
    
        fname = et.SubElement(p_info, 'file_name')
        fname.text = file_name
    
        system = et.SubElement(p_info, 'system')
        system.text = platform.uname()[0]
    
        node = et.SubElement(p_info, 'node')
        node.text = platform.uname()[1]
    
        release = et.SubElement(p_info, 'release')
        release.text = platform.uname()[2]
    
        version = et.SubElement(p_info, 'version')
        version.text = platform.uname()[3]
    
        machine = et.SubElement(p_info, 'machine')
        machine.text = platform.uname()[4]
    
        processor = et.SubElement(p_info, 'processor')
        processor.text = platform.uname()[5]
    
        run_time_stamp = et.SubElement(p_info, 'run_time_stamp')
        run_time_stamp.text = datetime.datetime.now().isoformat()
    
        desc_el = et.SubElement(p_info, 'desc')
        desc_el.text = desc
    
        if write_generator_info:
            repo = git.Repo(search_parent_directories=True)
            if repo.is_dirty():
                raise RuntimeError('Repository not up-to-date')
    
            g_info = et.SubElement(p_info, 'generator_info')
            generator_file = et.SubElement(g_info, 'generator_file')
            if generator_file_name is None:
                frame = inspect.stack()[1]
                generator_file_name = frame[0].f_code.co_filename
            generator_file.text = generator_file_name
    
            commit = et.SubElement(g_info, 'commit')
            commit.text = repo.head.object.hexsha
    
            if generator_args is not None:
                arg_info = et.SubElement(g_info, 'arg_info')
                if isinstance(generator_args, argparse.Namespace):
                    generator_args_dict = vars(generator_args)
                elif isinstance(generator_args, dict):
                    generator_args_dict = generator_args
                else:
                    raise ValueError('generator_args: Unrecognized format')
    
                arg_flags = generator_args_dict.keys()
                for a in arg_flags:
                    arg_el = et.SubElement(arg_info, a)
                    if generator_args_dict[a] is not None and \
                       generator_args_dict[a] not in file_names:
                        if os.path.isfile(str(generator_args_dict[a])):
                            if str(generator_args_dict[a]) not in file_names:
                                insert_dependency_file_info(arg_el,
                                    str(generator_args_dict[a]))
                        else:
                            arg_el.text = str(generator_args_dict[a])
    
            if aux_file_deps is not None:
                aux_info = et.SubElement(g_info, 'aux_file_info')
                for k in aux_file_deps.keys():
                    aux_el = et.SubElement(aux_info, k)
                    if aux_file_deps[k] is not None:
                        if os.path.isfile(str(aux_file_deps[k])):
                            if str(aux_file_deps[k]) not in file_names:
                                insert_dependency_file_info(aux_el,
                                    str(aux_file_deps[k]))


        tree = et.ElementTree()
        tree._setroot(p_info)
        tree.write(file_name + '.provenance_info.xml', xml_declaration=True)

if __name__ == '__main__':
    desc = """Generate provenace information for the specified file. Provenance
    information for file 'f' will be stored in 'f.provenance_info.xml'"""

    parser = ArgumentParser(description=desc)
    parser.add_argument('-f',
        help='File for which to generate provenance information', dest='f', \
        metavar='<string>', default=None)
    parser.add_argument('--aux_file_deps',
        help='In some cases, a file might depend on other data files but may \
        itself be generated by third-party software that makes it difficult \
        to seemless track provenance information across the processing \
        pipeline. By specifying here a comma-separated list of file names \
        (including the complete paths) on which a third-party processing \
        operation depends, we can partially track information necessary to \
        recreate the data file. Note, however, that this is not optimal. \
        Ideally, one would also want to track all details of the processing \
        operation itself (parameter settings, code version, etc), but this \
        can be challenging in certain special circumstances.',
        dest='aux_file_deps', metavar='<string>', default=None)

    op = parser.parse_args()

    write_provenance_data(op.f, write_generator_info=False,
                          aux_file_deps=op.aux_file_deps)
