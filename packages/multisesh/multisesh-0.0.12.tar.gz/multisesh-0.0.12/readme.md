# MultiSesh

This package provides a framework for working with microscopy data that has been obtained over multiple sessions. That is, it helps processing data when you may have run many different microscopy routines over the course of one experiment with varying imaging parameters.

The processing currently includes tile stitching, time labelling, z-projection, alignment, region extraction.

Some other basic processing it can do are:  
-simple image size reduction  
-deletion of blank time points (e.g. incomplete sessions/crashes)  
-field of view homogenisation - you provide a 'filter image' of how the field of view sensitivity varies  
-auto levels

As an example, a task it would be particularly useful for is extracting intensity profiles from corresponding regions over a long experiment where lots of things changed and moved over the course of the experiment. Or to make a summary video of a similar such experiment.

## The class rationale of the API

The API defines 4 classes: XFold, Session, TFile, TData. They have a hierarchical structure, with XFold containing the most global data down to TData with the most specific.

XFold stores the path to the directory that contains all the raw data. This raw data will never be changed by the package.

XFold also stores a list of all the Sessions (see below) that can be found in the XFold directory. By default they are ordered by their start time.

XFold also has methods to show you summary statistics gathered from the whole experiment. Stuff like how many time points, what channels etc.

The last thing XFold contains is various counters that can be updated by any analysis that you run and that you can print at the end of an analysis.

So overall there is very little data in the XFold but the idea is that it represents the global experiment folder and a complete script will only need users to define this object.

Session stores the details of a particularly microscopy session, that is, a particular time you have pressed run and the microscope software has run a routine.

It stores the session metadata, because this might change between sessions but must be the same for all files that come from that session. This includes start time, time point interval, number of time points and fields and montage tiles etc.

It also contains a list of all the TFiles (see below) associated with the Session.

It also contains the parent XFold, so you can move back up the class hierarchy. And the session number, showing where it can be found in the parent XFold's list of session.

A TFile corresponds to an individual file in the experiment folder containing image data. But it still doesn't hold the actual data! It contains the path to that file, the parent Session and what part of that session's data it holds (i.e. which time points and fields). Note that in general you have to open the file to know what data points it contains (i.e. relative to the session), so doing this once when building the TFile saves processing time.

The TData is the lowest level class and the one that actually holds the image data. The data is a 7D numpy array with axes order (times,fields,montages,z-slices,channels,y,x). You can build a TData from a Session or a TFile and it doesn't have to contain all the data of that object, i.e. you can pull out specific time points/channels etc. TDatas therefore help with memory management. When you build a TData from a Session it can come from multiple TFiles.

Note how you can't build a TData from an XFold, i.e. not from multiple sessions. This is because different Sessions maybe have differentsized dimensions (e.g. different number of z-slices) so you would end up with a jagged array which numpy doesn't handle.

TDatas also hold the parent TFiles and Session, and the information of where in the Session you have taken that data from, i.e. which time point/field etc.

All the important processing methods are methods of TData.


## The analysis rationale of the API

A general data processing script will proceed as follows:

- build the XFold.

- loop over all Sessions in the XFold and usually over all separate time points and fields in the session.

- in each iteration create a TData and apply a sequence of processing functions to that TData and then save it.

One important restriction on how you can use the API - your output is disconnected from the XFold framework once you save a TData - you can't reanalyse an analysed file. This is because we don't yet save the output with enough metadata to create a new XFold from that analysed data. To help a little with this we define a small 5th Class: OutDir. With that you can do some very limited processing on the saved files output by this package, such as concatenation and levels.


## Some important parameters

FieldIDMapList - This gives a name to each field in each session. It allows you to control what fields the packages treat as which of your experiments, in case this changes from session to session. You can leave as default which is that each field i in the data corresponds to your experiment i.

Filters - a list of strings, and files including any of these strings in their name will be ignored.

StartTimes - This allows you to specify a reference time for each field in the XFold, e.g. to use as that experiment's starting time or a stimulation time.
