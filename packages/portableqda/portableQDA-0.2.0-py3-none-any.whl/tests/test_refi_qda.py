"""
# @Time    : 12/2/2021 15:07
# @Author  : leandro.batlle@gmail.com
# @File    : test_refi_qda.py

"""

from portableqda.refi_qda import codeSetDict, codebookCls, etree, ENCODING, codeCls, setCls
import portableqda
import nose


import logging,sys
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
portableqda.refi_qda.log.addHandler(handler)
portableqda.log.setLevel(logging.DEBUG)

#@nose.SkipTest
def test_codeSetDict_class():
    """
    class codeSetDict indexes members of the CodeBook. See comments here

    :return:
    """

    #
    #  codeSetDict constructor needs a list for memberTypes
    #
    try:
        myCodeSetDict = codeSetDict(memberTypes=None)
    except ValueError as e:
        if str(e).find("sequence") == -1:
            raise
    myCodeSetDict = codeSetDict(memberTypes=(int, float))

    #
    #  codeSetDict constructor does not populate the underlying dict in any way
    #
    assert len(myCodeSetDict.keys()) == 0

    #
    # codeSetDict tells you if an item will be wellcomed
    #
    assert not myCodeSetDict.allowType(str)
    assert myCodeSetDict.allowType(int)

    #
    #  codeSetDict raises ValeuError when a new meber's type is not listed in memberTypes
    #
    try:
        myCodeSetDict["non-existant key"] = "bad type"
        pass
    except ValueError as e:
        if str(e).find("memberTypes") == -1:
            raise
        print("INFO: OK codeSetDict rejects new member with message '" + str(e) + "'")
    except Exception as e:
        raise
    else:
        raise NotImplementedError("class codeSetDict accepts types not in 'memberTypes'")

    #
    #  codeSetDict behaves as defaultDict
    #
    var = myCodeSetDict["non-existant key"]
    assert var is None
    assert "non-existant key" in myCodeSetDict.keys()
    myCodeSetDict["non-existant key"] = 10
    assert myCodeSetDict["non-existant key"] == 10
    myCodeSetDict["key2"] = myCodeSetDict["non-existant key"] / 2
    assert myCodeSetDict["key2"] == 5 / 1

    #
    # OK!
    #
    assert True


#@nose.SkipTest
def test_codebookCls_writeQdc():
    codebook = codebookCls()
    codebook.writeQdcFile()  # stdout
    codebook = codebookCls(output="portableQDA_test.qdc")  # home directory, all platforms
    codebook.writeQdcFile()


#@nose.SkipTest
def test_codebookCls_readQdc():
    codebook = codebookCls(output="portableQDA_test.qdc")
    codebook.writeQdcFile()
    codebook.readQdcFile(input="portableQDA_test.qdc")
    codebook.input = "portableQDA_test.qdc"
    codebook.readQdcFile()  # input param cis optional if already as object attribute
    pass


#@nose.SkipTest
def test_codebookCls_roundtrip_REFIQDA1_5():
    """
    test roudtrip import/export using the appendix A of the REFI-QDA 1.5 Standard (Sets tag added for completeness)

    see https://www.qdasoftware.org/wp-content/uploads/2019/09/REFI-QDA-1-5.pdf

    :return:
    """
    file = {"initial": "REFI-QDA-1-5.qdc",
            "intermediate": "REFI-QDA-1-5_test.qdc",
            "final": "REFI-QDA-1-5_test2.qdc"}
    codebook = codebookCls(output=file["intermediate"])
    codebook.readQdcFile(input=file["initial"])
    codebook.writeQdcFile()
    codebook2 = codebookCls(output=file["final"])
    codebook2.readQdcFile(input=file["intermediate"])
    codebook2.writeQdcFile()
    # compare the two outputs
    with open(codebook.output, encoding=ENCODING) as fh:
        with open(codebook2.output, encoding=ENCODING) as fh2:
            pass
            compare = fh.read() == fh2.read()
    assert compare
    # with open(codebook.output,mode="rb") as fh:
    #    codebook.tree2=etree.fromstring(fh.read())

    pass


#@nose.SkipTest
def test_codebookCls_roundtrip_atlasti():
    """
    test roundtrip import/export using a codebook from ATLAS.ti 9.0

    see https://www.atlasti.com

    :return:
    """
    file = {"initial": "portableQDA_Atlasti.qdc",
            "intermediate": "portableQDA_Atlasti_test2.qdc",
            "final": "portableQDA_Atlasti_test3.qdc"}
    codebook = codebookCls(output=file["intermediate"])
    codebook.readQdcFile(input=file["initial"])
    codebook.writeQdcFile()
    codebook2 = codebookCls(output=file["final"])
    codebook2.readQdcFile(input=file["intermediate"])
    codebook2.writeQdcFile()
    # compare the two outputs
    with open(codebook.output, encoding=ENCODING) as fh:
        with open(codebook2.output, encoding=ENCODING) as fh2:
            pass
            compare = fh.read() == fh2.read()
    assert compare
    # with open(codebook.output,mode="rb") as fh:
    #    codebook.tree2=etree.fromstring(fh.read())

    pass


def test_create_set():
    codebook = codebookCls()
    assert True


#@nose.SkipTest
def test_codebookCls_compareQdc():
    r=portableqda.resultCls
    codebookOld = codebookCls(output="portableQDA_compareQDC_Old.qdc")
    #
    # create two codebooks to compare
    #
    #  codebookOld = one code to delete (code1)
    #  codebookOld = one code and one set to keep  (___2)

    #set1 discard error state
    codebookOld.createElement(elementCls=setCls, #codebook elements are codeCls or setClas
                                                name="set1-Delete",
                                                description="set only in old codebook")
    set2=r(*codebookOld.createElement(elementCls=setCls, #codebook elements are codeCls or setClas
                                                name="set2-Common",
                                                description="set in both codebooks"))
    #check set2.error...
    error, errorDesc, code1 = codebookOld.createElement(elementCls=codeCls, name="code1-Delete",
                                                    description="code only in old codebook", sets=[set2.result.name,])
    code2 = r(*codebookOld.createElement(elementCls=codeCls, name="code2-Common",
                                                    description="test code  in both codebooks Desc", sets=None))
    #
    # New codebook
    #
    codebookNew = codebookCls(output="portableQDA_compareQDC_New.qdc")
    set2new=r(*codebookNew.createElement(elementCls=setCls, #codebook elements are codeCls or setClas
                                         name=set2.result.name,
                                         description=set2.result.description,
                                         guid=set2.result.attrib["guid"]))
    code2new = r(*codebookNew.createElement(elementCls=codeCls, name=code2.result.name+"-new name",
                                            description=code2.result.description+"-new name", guid=code2.result.attrib["guid"],
                                            sets=[set2new.result.name,]))
    code3 = r(*codebookNew.createElement(elementCls=codeCls, name="code3-New",
                                            description="code3 new to de new codebook",
                                            sets=[set2new.result.name,]))
    #
    # write codebooks
    #
    codebookOld.writeQdcFile()
    codebookNew.writeQdcFile()
    #
    # compare with no destination
    #
    portableqda.log.info("compareQDC with destination set to None (no postprocessing)")
    codebookOld.compareQdc(codebook=codebookNew, IamOlder=True, destination=None)
    codebookOld.writeQdcDiff(suffix="-DestinationDefault")

    #
    # compare with  destination="atlas9"
    #
    portableqda.log.info("compareQDC with destination (postprocessing) set atlas9")
    codebookOld.compareQdc(codebook=codebookNew, IamOlder=True, destination="atlas9")
    #codebookOld.writeQdcDiff(suffix=".qdc") #sub-testcase
    codebookOld.writeQdcDiff(suffix="-DestinationAtlas9.qdc")
