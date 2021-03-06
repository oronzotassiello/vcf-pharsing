import argparse
import sys
import gzip
from os.path import basename, join

import VCFAnnovarClass


def vcfnnvrprsr(argv):
    parser = argparse.ArgumentParser(usage='%(prog)s [options] arg1 arg2',
                                     description='Process vcf files.')
    parser.add_argument('vcf_file',
                        type=str,
                        help='vcf input file')
    parser.add_argument('-t',
                        '--type',
                        type=str,
                        dest='tissue_type',
                        action='store',
                        default="normal",
                        help='selct type of tissue [normal|tumor]')
    parser.add_argument('-q',
                        '--base_quality',
                        type=int,
                        dest='base_quality',
                        action='store',
                        default=0,
                        help='filter base quality [int]')
    parser.add_argument('--DP',
                        type=int,
                        dest='read_depth_arg',
                        action='store',
                        default=0,
                        help='filter read depth [int]')
    parser.add_argument('--AD',
                        type=int,
                        dest='variant_depth_arg',
                        action='store',
                        default=0,
                        help='filter variant depth[int]')
    parser.add_argument('-f',
                        '--mutation_frequency',
                        type=float,
                        dest='mutation_frequency',
                        action='store',
                        default=0.0,
                        help='filter mutation frequency [float]')
    parser.add_argument('--GPV',
                        type=float,
                        dest='gpv_threshold',
                        action='store',
                        default=0.0,
                        help='filter germline mutation p-value  [float]')
    parser.add_argument('--SPV',
                        type=float,
                        dest='spv_threshold',
                        action='store',
                        default=0.0,
                        help='filter somatic mutation p-value [float]')
    parser.add_argument('-a',
                        '--AAFreq',
                        type=float,
                        dest='allele_freq_threshold',
                        action='store',
                        default=0.0,
                        help='filter allele frequency percentage [float]')
    parser.add_argument('--out',
                        type=str,
                        dest='out_dir',
                        action='store',
                        default='.',
                        help='path of the output folder')

    args = parser.parse_args()

    # initiate the VCFAnnovar class object
    va = VCFAnnovarClass.VCFAnnovar(args.vcf_file)

    # create a output log file info
    log_sting = ("tissue type= %s \n"
                 "base quality= %d \n"
                 "mutation frequency= %.4f \n"
                 "GPV= %.4e \n"
                 "SPV= %.4e \n"
                 "read depth (DP)= %d \n"
                 "variant depth (AD)= %d \n"
                 "allele freq= %.4f \n") \
        % (args.tissue_type,
           args.base_quality,
           args.mutation_frequency,
           args.gpv_threshold,
           args.spv_threshold,
           args.read_depth_arg,
           args.variant_depth_arg,
           args.allele_freq_threshold)
    open(join(args.out_dir, "log.out"), 'w').write(log_sting)

    suffix = ".out"
    outfname = join(args.out_dir, basename(args.vcf_file) + suffix)

    if args.vcf_file.endswith(".gz"):
        with gzip.open(args.vcf_file, 'rb') as f:
            with gzip.open(outfname + ".gz", 'wb') as of:
                va.parsing(f, of, args)

    elif args.vcf_file.endswith(".vcf"):
        with open(args.vcf_file, 'r') as f:
            with open(outfname, 'w') as of:
                va.parsing(f, of, args)
    else:
        print ("unknown file format")


if __name__ == "__main__":
    vcfnnvrprsr(sys.argv[1:])
