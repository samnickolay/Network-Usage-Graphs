import sys
from os.path import isfile

import parse_logs
import make_plot
import modify_logs

def main():
    '''Main function'''

    if len(sys.argv) != 2:
        print("Received %d arguments - Expected 1" % (len(sys.argv) - 1))
        raise SystemExit

    file_name = sys.argv[1]

    # if len(sys.argv) > 2:
    #     print("Received %d arguments - Expected 1" % (len(sys.argv) - 1))
    #     raise SystemExit
    # elif len(sys.argv) is 2:
    #     file_name = sys.argv[1]
    # else:
    #     file_name = "globus_log.csv"

    print(file_name)

    if isfile(file_name) and file_name.endswith(".csv"):
        file_name = file_name
    elif isfile(file_name):
        print("Input file_name is not a .csv file - %s" % (file_name))
        raise SystemExit
    else:
        print("Input string is not a valid file_name - %s" % (file_name))
        raise SystemExit

    (header, transfers) = parse_logs.parse_csv(file_name, False)

    dict_transfers = parse_logs.dictify_rows(transfers)

    # transfers_by_day = parse_logs.get_transfers_by_day(dict_transfers, True)
    # transfers_per_day = parse_logs.get_transfers_per_day(dict_transfers, True)
    # max_date, max_count = parse_logs.get_max_day(dict_transfers, True)
    # transfers = parse_logs.get_transfers_on_day(dict_transfers, max_date)

    num_days_to_graph = 10
    num_bins = 86400

    top_transfer_days = parse_logs.get_busiest_days(dict_transfers, num_days_to_graph, True)

    for date, transfers in top_transfer_days.items():
        # plot_original_data(transfers, date, num_bins)

        plot_modified_data(transfers, date, num_bins)


def plot_original_data(transfers, date, num_bins):
    bins = modify_logs.bin_data(None, num_bins, transfers, date)

    title = "Network Usage on {} - {} Transfers".format(date, len(transfers))
    plot_filename = "plots/orig_network_demand/{}_{}-transfers_{}-bins.png".format(date, len(transfers), num_bins)
    make_plot.make_line_plot(plot_filename, title, bins)


def plot_modified_data(transfers, date, num_bins):
    min_price = 0.05
    max_price = 0.6
    non_flexible_jobs_percent = 0.5
    bins, x_bins, new_bins = modify_logs.split_logs_and_modify_transfers(num_bins, transfers, date, min_price,
                                                                         max_price, non_flexible_jobs_percent)

    title = "Network Usage on {} - {} Transfers".format(date, len(transfers))
    plot_filename = "plots/mod_network_demand/{}_{}-transfers_{}-bins.png".format(date, len(transfers), num_bins)
    make_plot.make_line_plot(plot_filename, title, bins, new_bins=new_bins)
    # make_plot.make_line_plot(plot_filename, title, bins, new_bins=new_bins, x_bins=x_bins)

    with open('output_logs/{}-transfers_{}.csv'.format(len(transfers), date), 'w') as the_file:
        for idx, cur_bin in enumerate(new_bins):
            the_file.write('{}, {}, {}, {}\n'.format(idx, cur_bin.start_t, cur_bin.end_t, cur_bin.bytes))


if __name__ == "__main__":
    main()
