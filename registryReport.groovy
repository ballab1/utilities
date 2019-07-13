import groovy.json.*

import java.awt.AttributeValue
import java.text.SimpleDateFormat
import java.util.Map


class RepoEntry {
    String digest
    String createTime
    ArrayList<String> tags = []

    //-------------------------------------
    RepoEntry(Object data) {
        digest = data.digest
        createTime = data.createTime
        tags = data.tags
    }

    //-------------------------------------
    String toString() {
        String out = '       ' + digest + ', ' + createTime + '\n'
        tags.sort().each { k ->
            out += '          ' + k.toString() + '\n'
        }
        out
    }

    //-------------------------------------
    int getNumTags() {
        tags.size()
    }
}

class RepoContents {
    String name
    String id
    ArrayList<RepoEntry> digests = []

    //-------------------------------------
    RepoContents(Object data) {
        name = data.repository
        id = data.id
        data.digests.each { x ->
            digests += new RepoEntry(x)
        }
    }

    //-------------------------------------
    int getNumTags() {
        int count = 0
        digests.each { it ->
            count += it.numTags
        }
        return count
    }

    //-------------------------------------
    int getNumImages() {
        digests.size()
    }

    //-------------------------------------
    String report() {
        String out = this.summary()
        digests.sort{it.createTime}.each { k ->
            out += k.toString() + '\n'
        }
        out
    }

    //-------------------------------------
    String summary() {
        return String.format('%4s: %-37s  Images: %-4s Tags: %3d\n', id, name+',', numImages+',', numTags)
    }
}

class JsonData {
    String base
    ArrayList<RepoContents> repos = []

    //-------------------------------------
    JsonData(String jsonFile) {
        Map json = readJson(jsonFile)
        parser(json)
    }

    //-------------------------------------
    private int getNumImages()
    {
        int imageCount = 0
        repos.each { r ->
            imageCount += r.numImages
        }
        return imageCount
    }

    //-------------------------------------
    private int getNumRepos()
    {
        return repos.size()
    }

    //-------------------------------------
    private int getNumTags()
    {
        int tagCount = 0
        repos.each { r ->
            tagCount += r.numTags
        }
        return tagCount
    }

    //-------------------------------------
    def parser(Map json) {
        json.data.each { k ->
            repos += new RepoContents(k)
        }
    }

    //-------------------------------------
    def readJson(String filename) {
        def jsonFileData = new File(filename)

        def slurper = new JsonSlurper()
        slurper.parseText('{"data":'+jsonFileData.text+'}')
    }

    //-------------------------------------
    String report() {
        def date = new Date()
        def sdf = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss")
        String out = '\nDate:  ' + sdf.format(date)
        out += '\n\nTotal number of repos:  ' + numRepos
        out += '\nTotal number of images: ' + numImages
        out += '\nTotal number of tags:   ' + numTags
        out += '\n\n===============================================================================\n'
        out += this.toString()
        out += '\n\n===============================================================================\n'
        repos.each { r ->
            out += r.report()
        }
        out
    }

    //-------------------------------------
    String toString() {
        String out = 'Summary:\n'
        repos.each { r ->
            out += r.summary()
        }
        out
    }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////
//
//     MAIN
//
//////////////////////////////////////////////////////////////////////////////////////////////////////////

def base = System.getenv('BASE') ?: '/home/groovy/scripts'
def jsonFile = System.getenv('JSON') ?: "${base}/registryReport.json"

def processor = new JsonData(jsonFile)
def out = new File("${base}/registryReport.txt")
if ( out.exists() ) {
    out.delete()
}
out << processor.report()

//println 'done.'

''
